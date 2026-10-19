#!/usr/bin/env python3
"""Validate and export BKL companion packages without changing host settings.

Only package-owned source is copied. Endpoint selection is explicit and never
fetches URLs, copies credentials, or edits an installed Plugin/cache. The output
marketplace is a new directory; existing paths are never replaced.
"""

import argparse
import copy
import hashlib
import ipaddress
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "banyan-knowledge-lite"
SOURCE = ROOT / "plugins" / PLUGIN_NAME
SKILLS = ("bk-setup", "bk-recall", "bk-capture", "bk-maintain")
PROFILES = {
    "recall": ["bk.memory.read", "offline_access"],
    "capture": ["bk.memory.read", "bk.memory.write", "bk.project.write", "offline_access"],
    "propose": ["bk.memory.read", "bk.memory.propose", "offline_access"],
    "govern": ["bk.memory.read", "bk.memory.govern", "offline_access"],
}


def read_json(path):
    """Read UTF-8 JSON; malformed source must fail rather than be defaulted."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    """Write a generated manifest under a newly created staging directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_files(source):
    """Enumerate contained regular package files, rejecting symlinks and caches."""
    paths = sorted(source.rglob("*"))
    for path in paths:
        if path.is_symlink():
            raise ValueError(f"Package symlinks are not allowed: {path.name}")
        if path.name in ("__pycache__", "node_modules", ".env", ".git"):
            raise ValueError(f"Unexpected package content: {path.name}")
    return [path for path in paths if path.is_file()]


def synchronize_compatibility(directory):
    """Project portable manifests into the existing Codex compatibility layout."""
    manifest = read_json(directory / "plugin.json")
    legacy = {key: value for key, value in manifest.items() if key not in ("$schema", "extensions")}
    legacy["skills"] = "./skills/"
    legacy["interface"] = manifest["extensions"]["com.openai"]["interface"]
    if (directory / "mcp.json").exists():
        legacy["mcpServers"] = "./.mcp.json"
        portable = read_json(directory / "mcp.json")
        write_json(directory / ".mcp.json", {"mcpServers": portable["mcpServers"]})
    write_json(directory / ".codex-plugin" / "plugin.json", legacy)


def validate(source=SOURCE):
    """Check the repository's manifest/skill contract, not a host certification."""
    files = source_files(source)
    expected = {"plugin.json", "mcp.json", ".mcp.json", ".codex-plugin/plugin.json"}
    expected.update(f"skills/{name}/SKILL.md" for name in SKILLS)
    if {path.relative_to(source).as_posix() for path in files} != expected:
        raise ValueError("Unexpected or missing package files; update the explicit package contract first")
    manifest = read_json(source / "plugin.json")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Missing portable Plugin schema declaration")
    if manifest.get("name") != PLUGIN_NAME or not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        raise ValueError("Unexpected Plugin identity or version")
    interface = manifest["extensions"]["com.openai"]["interface"]
    if not 1 <= len(interface["shortDescription"]) <= 30:
        raise ValueError("Plugin subtitle must contain 1–30 characters")
    legacy = read_json(source / ".codex-plugin" / "plugin.json")
    for key in ("name", "version", "description", "author", "homepage", "repository"):
        if legacy.get(key) != manifest.get(key):
            raise ValueError(f"Compatibility manifest differs: {key}")
    if legacy.get("interface") != interface or legacy.get("skills") != "./skills/" or legacy.get("mcpServers") != "./.mcp.json":
        raise ValueError("Compatibility components differ")
    mcp = read_json(source / "mcp.json")
    if mcp.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
        raise ValueError("Missing portable MCP schema declaration")
    if set(mcp["mcpServers"]) != {PLUGIN_NAME}:
        raise ValueError("Unexpected MCP server set")
    server = mcp["mcpServers"][PLUGIN_NAME]
    local = server["extensions"]["com.openai"]["auth"].get("type") == "none"
    if server["type"] != "streamable-http":
        raise ValueError("Unexpected MCP transport")
    validate_endpoint(server["url"], local)
    if read_json(source / ".mcp.json") != {"mcpServers": mcp["mcpServers"]}:
        raise ValueError("Compatibility MCP config differs")
    auth = server["extensions"]["com.openai"]["auth"]
    if local:
        if auth != {"type": "none"}:
            raise ValueError("Local MCP must not request remote credentials")
    elif auth.get("type") != "oauth" or auth.get("client") != {"mode": "cimd"} or auth.get("defaultScopes") != [] or auth.get("baseScopes") not in PROFILES.values():
        raise ValueError("Unexpected OAuth profile")
    skill_paths = sorted((source / "skills").glob("*/SKILL.md"))
    if [path.parent.name for path in skill_paths] != sorted(SKILLS):
        raise ValueError("Expected exactly four BK skills")
    for path in skill_paths:
        body = path.read_text(encoding="utf-8")
        if not body.startswith(f"---\nname: {path.parent.name}\ndescription: ") or "\n---\n" not in body[4:]:
            raise ValueError(f"Invalid skill metadata: {path.parent.name}")
    return manifest


def validate_catalog():
    """Require the stable marketplace identity and contained, selectable source."""
    catalog = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    if catalog["name"] != "gpt-plugin-market-public":
        raise ValueError("Marketplace identity changed")
    entries = [entry for entry in catalog["plugins"] if entry["name"] == PLUGIN_NAME]
    if len(entries) != 1:
        raise ValueError("Expected exactly one BKL marketplace entry")
    entry = entries[0]
    if entry["source"] != {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"} or entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"} or entry["category"] != "Productivity":
        raise ValueError("Unexpected BKL marketplace source or install policy")


def validate_endpoint(value, local=False):
    """Allow HTTPS endpoints, or explicitly selected canonical loopback HTTP.

    Reject URL credentials, query/fragment, encoded path tricks and malformed
    authority. Local mode intentionally supports only Lite's read-only boundary.
    """
    if not isinstance(value, str) or not value or any(ord(char) <= 32 or ord(char) == 127 for char in value):
        raise ValueError("Endpoint must be an explicit URL without whitespace")
    parts = urlsplit(value)
    hostname = parts.hostname
    if not hostname or parts.username is not None or parts.password is not None or parts.query or parts.fragment or "?" in value or "#" in value:
        raise ValueError("Endpoint must not contain credentials, query or fragment")
    if parts.path != "/mcp" or "\\" in value:
        raise ValueError("Expected exact /mcp endpoint path")
    if parts.port is not None and not 1 <= parts.port <= 65535:
        raise ValueError("Invalid endpoint port")
    if parts.netloc.endswith(":"):
        raise ValueError("Empty endpoint port")
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        if len(hostname) > 253 or any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label) for label in hostname.split(".")):
            raise ValueError("Invalid endpoint hostname") from None
    if local:
        if parts.scheme != "http" or hostname not in ("localhost", "127.0.0.1", "::1"):
            raise ValueError("Local read-only mode requires canonical loopback HTTP")
    elif parts.scheme != "https":
        raise ValueError("Remote OAuth endpoints require HTTPS")
    return value


def configure(output, url, profile="recall", local=False):
    """Export a new local marketplace; never modify source or existing installs."""
    validate_endpoint(url, local)
    if profile not in PROFILES or (local and profile != "recall"):
        raise ValueError("Local mode supports recall only")
    validate()
    output = Path(output).absolute()
    if output.resolve().is_relative_to(SOURCE.resolve()):
        raise ValueError("Output must be outside the source Plugin")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Output already exists; choose a new directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    # mkdir is exclusive: a racing exporter cannot replace an existing output.
    output.mkdir()
    plugin = output / "plugins" / PLUGIN_NAME
    shutil.copytree(SOURCE, plugin)
    mcp = read_json(plugin / "mcp.json")
    server = mcp["mcpServers"][PLUGIN_NAME]
    server["url"] = url
    server["extensions"]["com.openai"]["auth"] = {"type": "none"} if local else {
        "type": "oauth", "client": {"mode": "cimd"},
        "baseScopes": PROFILES[profile], "defaultScopes": [],
    }
    write_json(plugin / "mcp.json", mcp)
    manifest = read_json(plugin / "plugin.json")
    manifest["description"] = "Project-scoped governed Claim workflows for your configured Banyan Knowledge Lite installation."
    manifest["extensions"]["com.openai"]["interface"]["longDescription"] = (
        f"Connect to your selected BK installation at {url}. Selected profile: "
        f"{'local read-only' if local else profile}. Includes setup, retrieval, "
        "authorized capture and lifecycle guidance. Skills cannot add missing "
        "capabilities, change trust or bypass Agent Host approvals."
    )
    write_json(plugin / "plugin.json", manifest)
    synchronize_compatibility(plugin)
    marketplace = {
        "name": "bkl-local", "interface": {"displayName": "Your BK Lite"},
        "plugins": [{
            "name": PLUGIN_NAME, "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_USE" if local else "ON_INSTALL"},
            "category": "Productivity",
        }],
    }
    write_json(output / ".agents" / "plugins" / "marketplace.json", marketplace)
    validate(plugin)
    return output


def write_archive(directory, archive):
    """Create one reproducible, contained Plugin ZIP, including hidden overlays."""
    files = source_files(directory)
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as package:
        for path in files:
            info = zipfile.ZipInfo(f"{directory.name}/{path.relative_to(directory).as_posix()}", (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            package.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(archive.suffix + ".sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return {"name": archive.name, "sha256": digest}


def package(output):
    """Build connection and skills-only exports from the same canonical skills."""
    manifest = validate()
    output = Path(output)
    if output.resolve().is_relative_to(SOURCE.resolve()):
        raise ValueError("Archive output must be outside the Plugin")
    output.mkdir(parents=True, exist_ok=True)
    version = manifest["version"]
    names = [f"banyan-knowledge-lite-plugin-{version}.zip", f"banyan-knowledge-skills-{version}.zip", "bkl-companion-receipt.json"]
    for name in names:
        if (output / name).exists() or (output / (name + ".sha256")).exists():
            raise FileExistsError("Release artifacts already exist; refusing overwrite")
    artifacts = [write_archive(SOURCE, output / names[0])]
    with tempfile.TemporaryDirectory(prefix="bkl-skills-") as stage:
        skills_only = Path(stage) / "banyan-knowledge-skills"
        shutil.copytree(SOURCE / "skills", skills_only / "skills")
        skills_manifest = copy.deepcopy(manifest)
        skills_manifest["name"] = "banyan-knowledge-skills"
        skills_manifest["description"] = "Four governed BK Claim workflows for an existing authorized MCP connection. No server connection or credentials are bundled."
        interface = skills_manifest["extensions"]["com.openai"]["interface"]
        interface["displayName"] = "Banyan Knowledge Skills"
        interface["longDescription"] = skills_manifest["description"]
        write_json(skills_only / "plugin.json", skills_manifest)
        synchronize_compatibility(skills_only)
        artifacts.append(write_archive(skills_only, output / names[1]))
    revision = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    write_json(output / names[2], {
        "schema": "bk.companion-release.v1", "pluginVersion": version,
        "validatedLiteVersion": "0.1.2-beta.2.2", "sourceRevision": revision,
        "artifacts": artifacts,
    })
    return artifacts


def main():
    """Command-line entry point; outputs non-secret status, never credential data."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    export = commands.add_parser("configure")
    export.add_argument("--url", required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--profile", choices=PROFILES, default="recall")
    export.add_argument("--local-read-only", action="store_true")
    build = commands.add_parser("package")
    build.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            validate()
            validate_catalog()
        elif args.command == "configure":
            configure(args.output, args.url, args.profile, args.local_read_only)
        else:
            package(args.output)
    except (ValueError, OSError, KeyError) as error:
        # URL validation errors intentionally do not include raw user input.
        parser.exit(2, f"BKL package operation failed: {error}\n")
    print("BKL package operation completed; no host configuration or credentials changed.")


if __name__ == "__main__":
    main()
