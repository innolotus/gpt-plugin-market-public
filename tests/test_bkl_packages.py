"""Executable boundary checks for BKL configuration and portable exports."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("bkl_packages", Path(__file__).resolve().parents[1] / "scripts" / "bkl_packages.py")
bkl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bkl)


class BklPackagesTests(unittest.TestCase):
    def test_marketplace_exposes_one_contained_bkl_source(self):
        bkl.validate_catalog()

    def test_canonical_plugin_preserves_identity_endpoint_and_old_authority(self):
        manifest = bkl.validate()
        self.assertEqual("0.1.3", manifest["version"])
        server = bkl.read_json(bkl.SOURCE / "mcp.json")["mcpServers"][bkl.PLUGIN_NAME]
        self.assertEqual("https://bk.ols01.starfield.com.au/mcp", server["url"])
        self.assertEqual(bkl.PROFILES["capture"], server["extensions"]["com.openai"]["auth"]["baseScopes"])

    def test_profile_authorities_do_not_imply_other_mutations(self):
        for profile, authority in (("recall", None), ("capture", "bk.memory.write"), ("propose", "bk.memory.propose"), ("govern", "bk.memory.govern")):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as stage:
                output = Path(stage) / "market"
                bkl.configure(output, "https://knowledge.example:8443/mcp", profile)
                plugin = output / "plugins" / bkl.PLUGIN_NAME
                bkl.validate(plugin)
                server = bkl.read_json(plugin / "mcp.json")["mcpServers"][bkl.PLUGIN_NAME]
                self.assertEqual("https://knowledge.example:8443/mcp", server["url"])
                scopes = server["extensions"]["com.openai"]["auth"]["baseScopes"]
                self.assertEqual(bkl.PROFILES[profile], scopes)
                for other in ("bk.memory.write", "bk.memory.propose", "bk.memory.govern"):
                    self.assertEqual(other == authority, other in scopes)
                self.assertEqual(profile == "capture", "bk.project.write" in scopes)
                text = (plugin / "plugin.json").read_text()
                self.assertNotIn("bk.ols01", text)
                self.assertNotIn("bk.ols01", (plugin / ".codex-plugin" / "plugin.json").read_text())

    def test_configure_defaults_to_read_only_remote_profile(self):
        with tempfile.TemporaryDirectory() as stage:
            output = bkl.configure(Path(stage) / "market", "https://my-bk.example/mcp")
            server = bkl.read_json(output / "plugins" / bkl.PLUGIN_NAME / "mcp.json")["mcpServers"][bkl.PLUGIN_NAME]
            self.assertEqual(bkl.PROFILES["recall"], server["extensions"]["com.openai"]["auth"]["baseScopes"])

    def test_explicit_local_mode_has_no_oauth_and_only_recall(self):
        for host in ("127.0.0.1", "localhost", "[::1]"):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as stage:
                output = bkl.configure(Path(stage) / "market", f"http://{host}:58080/mcp", local=True)
                plugin = output / "plugins" / bkl.PLUGIN_NAME
                bkl.validate(plugin)
                auth = bkl.read_json(plugin / "mcp.json")["mcpServers"][bkl.PLUGIN_NAME]["extensions"]["com.openai"]["auth"]
                self.assertEqual({"type": "none"}, auth)
        with tempfile.TemporaryDirectory() as stage:
            with self.assertRaises(ValueError):
                bkl.configure(Path(stage) / "market", "http://localhost:58080/mcp", "capture", True)
            self.assertFalse((Path(stage) / "market").exists())

    def test_invalid_endpoints_fail_before_creating_any_output(self):
        invalid = [
            "http://knowledge.example/mcp", "https://user:secret@knowledge.example/mcp",
            "https://knowledge.example/mcp?access_token=secret", "https://knowledge.example/mcp#secret",
            "https://knowledge.example/mcp?", "https://knowledge.example/mcp#",
            "https://knowledge.example/other", "https://knowledge.example/mcp/",
            "https://knowledge.example/%6dcp", "https://knowledge.example:70000/mcp",
            "https://knowledge.example:0/mcp", "https://knowledge.example:/mcp",
            "https://{host}/mcp", "https://knowledge.example\\evil/mcp",
            "https://knowledge.example/mcp\n", " https://knowledge.example/mcp",
            "https://bad_host/mcp", "file:///mcp", "ftp://knowledge.example/mcp",
        ]
        with tempfile.TemporaryDirectory() as stage:
            for index, url in enumerate(invalid):
                with self.subTest(url=url), self.assertRaises(ValueError):
                    bkl.configure(Path(stage) / str(index), url)
                self.assertFalse((Path(stage) / str(index)).exists())

    def test_local_mode_refuses_noncanonical_loopback_and_remote_hosts(self):
        for url in ("http://127.0.0.2/mcp", "http://localhost.evil.example/mcp", "http://192.168.1.2/mcp", "https://localhost/mcp"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                bkl.validate_endpoint(url, local=True)

    def test_export_does_not_overwrite_existing_destination_or_source(self):
        before = {path.relative_to(bkl.SOURCE): path.read_bytes() for path in bkl.source_files(bkl.SOURCE)}
        with tempfile.TemporaryDirectory() as stage:
            output = Path(stage) / "existing"
            output.mkdir()
            sentinel = output / "user.json"
            sentinel.write_text("user-owned")
            with self.assertRaises(FileExistsError):
                bkl.configure(output, "https://knowledge.example/mcp")
            self.assertEqual("user-owned", sentinel.read_text())
        with self.assertRaises(ValueError):
            bkl.configure(bkl.SOURCE / "recursive", "https://knowledge.example/mcp")
        self.assertEqual(before, {path.relative_to(bkl.SOURCE): path.read_bytes() for path in bkl.source_files(bkl.SOURCE)})

    def test_reproducible_archives_and_receipt_have_exact_source_skills(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a, b = bkl.package(first), bkl.package(second)
            self.assertEqual(a, b)
            for artifact in a:
                archive = Path(first) / artifact["name"]
                self.assertEqual(artifact["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())
                self.assertTrue(archive.with_suffix(".zip.sha256").read_text().startswith(artifact["sha256"]))
                with zipfile.ZipFile(archive) as package:
                    self.assertIsNone(package.testzip())
                    paths = package.namelist()
                    prefix = paths[0].split("/")[0]
                    self.assertTrue(all(path.startswith(prefix + "/") and ".." not in Path(path).parts for path in paths))
                    skill_paths = [path for path in paths if path.endswith("/SKILL.md")]
                    self.assertEqual(4, len(skill_paths))
                    for path in skill_paths:
                        relative = Path(path).relative_to(prefix)
                        self.assertEqual((bkl.SOURCE / relative).read_bytes(), package.read(path))
                    manifest = json.loads(package.read(prefix + "/plugin.json"))
                    self.assertEqual("0.1.3", manifest["version"])
                    self.assertIn(prefix + "/.codex-plugin/plugin.json", paths)
                    if prefix == "banyan-knowledge-skills":
                        self.assertFalse(any("mcp.json" in path for path in paths))
                        legacy = json.loads(package.read(prefix + "/.codex-plugin/plugin.json"))
                        self.assertNotIn("mcpServers", legacy)
                    else:
                        self.assertIn(prefix + "/mcp.json", paths)
                        self.assertIn(prefix + "/.mcp.json", paths)
            receipt = bkl.read_json(Path(first) / "bkl-companion-receipt.json")
            self.assertEqual(a, receipt["artifacts"])
            self.assertEqual(40, len(receipt["sourceRevision"]))
            with self.assertRaises(FileExistsError):
                bkl.package(first)

    def test_symlinks_and_compatibility_drift_are_rejected(self):
        with tempfile.TemporaryDirectory() as stage:
            source = Path(stage) / "plugin"
            bkl.shutil.copytree(bkl.SOURCE, source)
            legacy_path = source / ".mcp.json"
            legacy = bkl.read_json(legacy_path)
            legacy["mcpServers"][bkl.PLUGIN_NAME]["url"] = "https://other.example/mcp"
            bkl.write_json(legacy_path, legacy)
            with self.assertRaises(ValueError):
                bkl.validate(source)
            bkl.synchronize_compatibility(source)
            bkl.validate(source)
            (source / "escape").symlink_to(Path(stage))
            with self.assertRaises(ValueError):
                bkl.validate(source)


if __name__ == "__main__":
    unittest.main()
