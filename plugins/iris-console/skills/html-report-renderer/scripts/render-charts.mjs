#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const WIDTH = 960;
const HEIGHT = 540;
const MAX_CHARTS = 6;
const MAX_POINTS = 48;
const MAX_SERIES = 4;
const PALETTE = ["#e65300", "#9d3515", "#f2a65a", "#f7c98e"];
const SURFACE = "#ffffff";
const INK = "#24272a";
const MUTED = "#697077";
const GRID = "#e7e9eb";
const FILL = "#fbf8f6";
const ACCENT_SOFT = "#fff1e8";

function fail(message) {
  throw new Error(message);
}

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function number(value, context) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    fail(`${context} must be a finite number`);
  }
  if (Math.abs(value) > 1_000_000_000_000_000) {
    fail(`${context} exceeds the supported magnitude`);
  }
  return value;
}

function text(value, context, maxLength = 120) {
  if (typeof value !== "string" || value.trim() === "" || value.length > maxLength) {
    fail(`${context} must be a non-empty string no longer than ${maxLength} characters`);
  }
  return value.trim();
}

function list(value, context, maximum = MAX_POINTS) {
  if (!Array.isArray(value) || value.length < 1 || value.length > maximum) {
    fail(`${context} must contain between 1 and ${maximum} items`);
  }
  return value;
}

function formatValue(value, format = "number") {
  const sign = value < 0 ? "-" : "";
  const absolute = Math.abs(value);
  if (format === "aud") return `${sign}$${Math.round(absolute).toLocaleString("en-AU")}`;
  if (format === "aud-compact") {
    if (absolute >= 1_000_000) return `${sign}$${(absolute / 1_000_000).toFixed(2).replace(/0+$/, "").replace(/\.$/, "")}m`;
    if (absolute >= 1_000) return `${sign}$${(absolute / 1_000).toFixed(1).replace(/\.0$/, "")}k`;
    return `${sign}$${Math.round(absolute)}`;
  }
  if (format === "percent") return `${(value * 100).toFixed(2).replace(/0+$/, "").replace(/\.$/, "")}%`;
  return value.toLocaleString("en-AU", { maximumFractionDigits: 2 });
}

function compactLabel(value, maximum) {
  const characters = Array.from(value);
  return characters.length <= maximum ? value : `${characters.slice(0, maximum - 1).join("")}…`;
}

function provenanceText(provenance) {
  return `${provenance.unit} · ${provenance.period} · ${provenance.returnBasis} · ${provenance.taxTreatment}`;
}

function chartFrame(chart, body, description) {
  const title = escapeXml(chart.title);
  const subtitle = chart.subtitle ? escapeXml(chart.subtitle) : "";
  const titleId = `${chart.id}-title`;
  const descId = `${chart.id}-desc`;
  return `<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${titleId} ${descId}" viewBox="0 0 ${WIDTH} ${HEIGHT}" width="${WIDTH}" height="${HEIGHT}" style="font-variant-numeric:tabular-nums;text-rendering:optimizeLegibility">
  <title id="${titleId}">${title}</title>
  <desc id="${descId}">${escapeXml(`${description} Basis: ${provenanceText(chart.provenance)}. Canonical fields: ${chart.provenance.fields.join(", ")}.`)}</desc>
  <rect width="${WIDTH}" height="${HEIGHT}" rx="24" fill="${SURFACE}"/>
  <rect x="1" y="1" width="${WIDTH - 2}" height="${HEIGHT - 2}" rx="23" fill="none" stroke="${GRID}"/>
  <rect x="48" y="30" width="44" height="5" rx="2.5" fill="${PALETTE[0]}"/>
  <text x="48" y="68" fill="${INK}" font-family="system-ui, sans-serif" font-size="28" font-weight="760" letter-spacing="-0.5">${title}</text>
  ${subtitle ? `<text x="48" y="94" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="14.5">${subtitle}</text>` : ""}
  ${body}
  <line x1="48" y1="493" x2="912" y2="493" stroke="${GRID}"/>
  <text x="48" y="517" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="11.5">${escapeXml(chart.provenance.unit)}</text>
  <text x="268" y="517" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="11.5">${escapeXml(chart.provenance.period)}</text>
  <text x="520" y="517" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="11.5">${escapeXml(chart.provenance.returnBasis)}</text>
  <text x="710" y="517" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="11.5">${escapeXml(chart.provenance.taxTreatment)}</text>
</svg>`;
}

function niceStep(rawStep) {
  const magnitude = 10 ** Math.floor(Math.log10(rawStep));
  const residual = rawStep / magnitude;
  const factor = residual <= 1.5 ? 1 : residual <= 2.25 ? 2 : residual <= 3.5 ? 2.5 : residual <= 7.5 ? 5 : 10;
  return factor * magnitude;
}

function extent(values, includeZero = false) {
  let min = Math.min(...values);
  let max = Math.max(...values);
  if (includeZero) {
    min = Math.min(0, min);
    max = Math.max(0, max);
  }
  if (min === max) max = min + Math.max(1, Math.abs(min) * 0.1);
  const rawRange = max - min;
  if (!includeZero) {
    min -= rawRange * 0.08;
    max += rawRange * 0.08;
  }
  const step = niceStep((max - min) / 4);
  min = Math.floor(min / step) * step;
  max = Math.ceil(max / step) * step;
  const ticks = [];
  for (let value = min; value <= max + step * 0.001; value += step) ticks.push(Math.abs(value) < step * 0.001 ? 0 : value);
  return { min, max, ticks };
}

function renderAxes({ left, top, plotWidth, plotHeight, min, max, ticks, format, labels, xLabelLength = 18, xMode = "points", xLabelStride = 1 }) {
  const y = (value) => top + plotHeight - ((value - min) / (max - min)) * plotHeight;
  const x = (index) => xMode === "groups"
    ? left + (plotWidth * (index + 0.5)) / labels.length
    : left + (labels.length === 1 ? plotWidth / 2 : (plotWidth * index) / (labels.length - 1));
  const grid = ticks.map((tick) => {
    const py = y(tick);
    return `<line x1="${left}" y1="${py.toFixed(2)}" x2="${left + plotWidth}" y2="${py.toFixed(2)}" stroke="${GRID}" stroke-dasharray="3 7"/>
    <text x="${left - 16}" y="${(py + 5).toFixed(2)}" text-anchor="end" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="13.5">${escapeXml(formatValue(tick, format))}</text>`;
  }).join("\n");
  const xLabels = labels
    .map((label, index) => ({ label, index }))
    .filter(({ index }) => index % xLabelStride === 0 || index === labels.length - 1)
    .map(({ label, index }) => `<text data-x-label-index="${index}" x="${x(index).toFixed(2)}" y="${top + plotHeight + 30}" text-anchor="middle" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="13.5"><title>${escapeXml(label)}</title>${escapeXml(compactLabel(label, xLabelLength))}</text>`)
    .join("\n");
  const plot = `<rect x="${left}" y="${top}" width="${plotWidth}" height="${plotHeight}" rx="14" fill="${FILL}"/>`;
  return { y, x, svg: `${plot}\n${grid}\n${xLabels}` };
}

function validateSeries(chart, maximumLabels = MAX_POINTS) {
  const labels = list(chart.labels, `${chart.id}.labels`, maximumLabels).map((label, index) => text(label, `${chart.id}.labels[${index}]`, 40));
  const series = list(chart.series, `${chart.id}.series`, MAX_SERIES).map((item, seriesIndex) => {
    const name = text(item?.name, `${chart.id}.series[${seriesIndex}].name`, 50);
    const values = list(item?.values, `${chart.id}.series[${seriesIndex}].values`)
      .map((value, valueIndex) => number(value, `${chart.id}.series[${seriesIndex}].values[${valueIndex}]`));
    if (values.length !== labels.length) fail(`${chart.id}.series[${seriesIndex}] must match labels length`);
    return { name, values };
  });
  return { labels, series };
}

function renderLine(chart) {
  const { labels, series } = validateSeries(chart);
  const values = series.flatMap((item) => item.values);
  const { min, max, ticks } = extent(values);
  const left = 104;
  const top = 154;
  const plotWidth = 796;
  const plotHeight = 276;
  const axes = renderAxes({ left, top, plotWidth, plotHeight, min, max, ticks, format: chart.format, labels });
  const paths = series.map((item, seriesIndex) => {
    const color = PALETTE[seriesIndex];
    const points = item.values.map((value, index) => `${axes.x(index).toFixed(2)},${axes.y(value).toFixed(2)}`);
    const circles = item.values.map((value, index) => `<circle cx="${axes.x(index).toFixed(2)}" cy="${axes.y(value).toFixed(2)}" r="4.5" fill="${SURFACE}" stroke="${color}" stroke-width="3"><title>${escapeXml(item.name)}: ${escapeXml(formatValue(value, chart.format))}</title></circle>`).join("\n");
    return `<polyline points="${points.join(" ")}" fill="none" stroke="${color}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"${seriesIndex % 2 === 1 ? ' stroke-dasharray="11 8"' : ""}/>${circles}`;
  }).join("\n");
  const legendWidth = Math.min(360, 790 / series.length);
  const legend = series.map((item, index) => {
    const lastValue = item.values.at(-1);
    const x = left + index * legendWidth;
    return `<g transform="translate(${x} 124)">
      <line x1="0" y1="0" x2="26" y2="0" stroke="${PALETTE[index]}" stroke-width="4"${index % 2 === 1 ? ' stroke-dasharray="8 5"' : ""}/>
      <text x="38" y="5" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="13.5">${escapeXml(item.name)}</text>
      <text x="178" y="5" fill="${INK}" font-family="system-ui, sans-serif" font-size="15" font-weight="720">${escapeXml(formatValue(lastValue, chart.format))}</text>
    </g>`;
  }).join("\n");
  return chartFrame(chart, `${legend}\n${axes.svg}\n${paths}`, `${chart.title}. ${series.map((item) => `${item.name}: ${item.values.map((value, index) => `${labels[index]} ${formatValue(value, chart.format)}`).join(", ")}`).join(". ")}`);
}

function renderBar(chart) {
  const { labels, series } = validateSeries(chart);
  const values = series.flatMap((item) => item.values);
  const { min, max, ticks } = extent(values, true);
  const left = 104;
  const top = 144;
  const plotWidth = 796;
  const plotHeight = 286;
  const axes = renderAxes({
    left,
    top,
    plotWidth,
    plotHeight,
    min,
    max,
    ticks,
    format: chart.format,
    labels,
    xLabelLength: 12,
    xMode: "groups",
    xLabelStride: Math.max(1, Math.ceil(labels.length / 8))
  });
  const groupWidth = plotWidth / labels.length;
  const barWidth = Math.min(90, (groupWidth * 0.68) / series.length);
  const barGap = Math.min(6, Math.max(1, barWidth * 0.18));
  const visibleBarWidth = Math.max(1, barWidth - barGap);
  const zeroY = axes.y(0);
  const bars = series.flatMap((item, seriesIndex) => item.values.map((value, labelIndex) => {
    const center = axes.x(labelIndex);
    const x = center - (barWidth * series.length) / 2 + seriesIndex * barWidth + barGap / 2;
    const valueY = axes.y(value);
    const y = Math.min(zeroY, valueY);
    const height = Math.max(2, Math.abs(zeroY - valueY));
    const valueLabel = formatValue(value, chart.format);
    const labelFits = height >= 32 && visibleBarWidth >= Math.max(28, valueLabel.length * 7.5);
    const label = labelFits
      ? `<text data-bar-value-label="true" x="${(x + visibleBarWidth / 2).toFixed(2)}" y="${(y + height / 2 + 5).toFixed(2)}" text-anchor="middle" fill="${SURFACE}" font-family="system-ui, sans-serif" font-size="14" font-weight="760">${escapeXml(valueLabel)}</text>`
      : "";
    return `<rect data-bar-label-index="${labelIndex}" data-bar-series-index="${seriesIndex}" x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${visibleBarWidth.toFixed(2)}" height="${height.toFixed(2)}" rx="${Math.min(8, visibleBarWidth / 2).toFixed(2)}" fill="${PALETTE[seriesIndex]}"><title>${escapeXml(item.name)}: ${escapeXml(valueLabel)}</title></rect>
    ${label}`;
  })).join("\n");
  const zero = `<line data-zero-baseline="true" x1="${left}" y1="${zeroY.toFixed(2)}" x2="${left + plotWidth}" y2="${zeroY.toFixed(2)}" stroke="${INK}" stroke-width="2"/>`;
  return chartFrame(chart, `${axes.svg}\n${zero}\n${bars}`, `${chart.title}. ${series.map((item) => `${item.name}: ${item.values.map((value, index) => `${labels[index]} ${formatValue(value, chart.format)}`).join(", ")}`).join(". ")}`);
}

function polar(cx, cy, radius, angle) {
  const radians = ((angle - 90) * Math.PI) / 180;
  return { x: cx + radius * Math.cos(radians), y: cy + radius * Math.sin(radians) };
}

function arcPath(cx, cy, outerRadius, innerRadius, startAngle, endAngle) {
  const startOuter = polar(cx, cy, outerRadius, endAngle);
  const endOuter = polar(cx, cy, outerRadius, startAngle);
  const startInner = polar(cx, cy, innerRadius, startAngle);
  const endInner = polar(cx, cy, innerRadius, endAngle);
  const largeArc = endAngle - startAngle > 180 ? 1 : 0;
  return `M ${startOuter.x} ${startOuter.y} A ${outerRadius} ${outerRadius} 0 ${largeArc} 0 ${endOuter.x} ${endOuter.y} L ${startInner.x} ${startInner.y} A ${innerRadius} ${innerRadius} 0 ${largeArc} 1 ${endInner.x} ${endInner.y} Z`;
}

function renderDonut(chart) {
  if (chart.mutuallyExclusive !== true) fail(`${chart.id}.mutuallyExclusive must be true`);
  const whole = number(chart.whole, `${chart.id}.whole`);
  if (whole <= 0) fail(`${chart.id}.whole must be greater than zero`);
  const wholeLabel = text(chart.wholeLabel, `${chart.id}.wholeLabel`, 50);
  const segments = list(chart.segments, `${chart.id}.segments`, 8).map((segment, index) => ({
    label: text(segment?.label, `${chart.id}.segments[${index}].label`, 50),
    value: number(segment?.value, `${chart.id}.segments[${index}].value`)
  }));
  if (segments.some((segment) => segment.value <= 0)) fail(`${chart.id}.segments values must be greater than zero`);
  const total = segments.reduce((sum, segment) => sum + segment.value, 0);
  const tolerance = Math.max(0.01, Math.abs(whole) * 1e-9);
  if (Math.abs(total - whole) > tolerance) fail(`${chart.id}.segments must sum to whole`);
  const cx = 286;
  const cy = 292;
  const outerRadius = 140;
  const innerRadius = 88;
  let angle = 0;
  const arcs = segments.map((segment, index) => {
    const start = angle;
    angle += (segment.value / total) * 360;
    return `<path d="${arcPath(cx, cy, outerRadius, innerRadius, start, angle)}" fill="${PALETTE[index % PALETTE.length]}" stroke="${SURFACE}" stroke-width="5"><title>${escapeXml(segment.label)}: ${escapeXml(formatValue(segment.value, chart.format))}</title></path>`;
  }).join("\n");
  const legendTop = 160;
  const legendHeight = 276;
  const rowHeight = legendHeight / segments.length;
  const legend = segments.map((segment, index) => {
    const y = legendTop + rowHeight * index + rowHeight / 2;
    const percent = `${((segment.value / total) * 100).toFixed(1)}%`;
    return `<rect data-donut-legend-index="${index}" x="510" y="${(y - 9).toFixed(2)}" width="18" height="18" rx="5" fill="${PALETTE[index % PALETTE.length]}"><title>${escapeXml(segment.label)}</title></rect>
    <text data-donut-legend-index="${index}" x="540" y="${(y + 5).toFixed(2)}" fill="${INK}" font-family="system-ui, sans-serif" font-size="14" font-weight="700"><title>${escapeXml(segment.label)}</title>${escapeXml(compactLabel(segment.label, 24))}</text>
    <text data-donut-legend-index="${index}" x="790" y="${(y + 5).toFixed(2)}" text-anchor="end" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="13.5">${escapeXml(formatValue(segment.value, chart.format))}</text>
    <text data-donut-legend-index="${index}" x="870" y="${(y + 5).toFixed(2)}" text-anchor="end" fill="${PALETTE[index % PALETTE.length]}" font-family="system-ui, sans-serif" font-size="13.5" font-weight="720">${percent}</text>`;
  }).join("\n");
  const center = `<circle cx="${cx}" cy="${cy}" r="75" fill="${ACCENT_SOFT}"/>
  <text x="${cx}" y="${cy - 8}" text-anchor="middle" fill="${MUTED}" font-family="system-ui, sans-serif" font-size="14"><title>${escapeXml(wholeLabel)}</title>${escapeXml(compactLabel(wholeLabel, 18))}</text>
  <text x="${cx}" y="${cy + 27}" text-anchor="middle" fill="${INK}" font-family="system-ui, sans-serif" font-size="25" font-weight="780">${escapeXml(formatValue(whole, chart.format))}</text>`;
  const legendPanel = `<rect x="486" y="138" width="408" height="320" rx="16" fill="${FILL}"/>`;
  return chartFrame(chart, `${legendPanel}\n${arcs}\n${center}\n${legend}`, `${chart.title}. ${segments.map((segment) => `${segment.label} ${formatValue(segment.value, chart.format)}`).join(", ")}. Total ${formatValue(total, chart.format)}.`);
}

function validateProvenance(raw, context) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail(`${context} must be an object`);
  return {
    canonicalReportReference: text(raw.canonicalReportReference, `${context}.canonicalReportReference`, 240),
    fields: list(raw.fields, `${context}.fields`, 12).map((field, index) => text(field, `${context}.fields[${index}]`, 180)),
    unit: text(raw.unit, `${context}.unit`, 40),
    period: text(raw.period, `${context}.period`, 80),
    returnBasis: text(raw.returnBasis, `${context}.returnBasis`, 60),
    taxTreatment: text(raw.taxTreatment, `${context}.taxTreatment`, 80)
  };
}

function validateChart(raw, index) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail(`charts[${index}] must be an object`);
  const id = text(raw.id, `charts[${index}].id`, 64);
  if (!/^[a-z0-9][a-z0-9-]*$/.test(id)) fail(`charts[${index}].id must use lowercase letters, digits and hyphens`);
  const type = text(raw.type, `charts[${index}].type`, 12);
  if (!["line", "bar", "donut"].includes(type)) fail(`charts[${index}].type must be line, bar or donut`);
  const format = raw.format ?? "number";
  if (!["number", "aud", "aud-compact", "percent"].includes(format)) fail(`charts[${index}].format is unsupported`);
  return {
    ...raw,
    id,
    type,
    title: text(raw.title, `charts[${index}].title`),
    subtitle: raw.subtitle ? text(raw.subtitle, `charts[${index}].subtitle`, 160) : "",
    format,
    provenance: validateProvenance(raw.provenance, `charts[${index}].provenance`)
  };
}

async function readStdin() {
  let source = "";
  for await (const chunk of process.stdin) source += chunk;
  if (source.length > 1_000_000) fail("chart specification exceeds 1 MB");
  try {
    return JSON.parse(source);
  } catch (error) {
    fail(`chart specification is not valid JSON: ${error.message}`);
  }
}

function outputDirectory(argv) {
  const index = argv.indexOf("--output-dir");
  if (index < 0 || !argv[index + 1]) fail("usage: render-charts.mjs --output-dir <directory>");
  return path.resolve(argv[index + 1]);
}

async function main() {
  const directory = outputDirectory(process.argv.slice(2));
  const payload = await readStdin();
  const charts = list(payload?.charts, "charts", MAX_CHARTS).map(validateChart);
  const ids = new Set(charts.map((chart) => chart.id));
  if (ids.size !== charts.length) fail("chart ids must be unique");
  await mkdir(directory, { recursive: true });
  const artifacts = [];
  for (const chart of charts) {
    const svg = chart.type === "line" ? renderLine(chart) : chart.type === "bar" ? renderBar(chart) : renderDonut(chart);
    const file = path.join(directory, `${chart.id}.svg`);
    await writeFile(file, svg, { encoding: "utf8", flag: "wx" });
    artifacts.push({ id: chart.id, type: chart.type, path: file });
  }
  process.stdout.write(`${JSON.stringify({ charts: artifacts }, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`render-charts: ${error.message}\n`);
  process.exitCode = 1;
});
