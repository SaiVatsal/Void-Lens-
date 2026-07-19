"""
VoidLens formatter — export scan results to JSON, CSV, HTML, Markdown, XML, SARIF.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from voidlens.core.models import ScanResult


def to_json(results: list[ScanResult], pretty: bool = True) -> str:
    """Serialize scan results to JSON string."""
    data = [r.to_dict() for r in results]
    return json.dumps(data, indent=2 if pretty else None, ensure_ascii=False)


def to_csv(results: list[ScanResult]) -> str:
    """Serialize scan results to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Query", "Type", "Site", "Category", "Status", "URL", "Reason", "Response Time"])
    for result in results:
        for site in result.results:
            writer.writerow([
                result.query,
                result.scan_type.value,
                site.site,
                site.category,
                site.status.value,
                site.url,
                site.reason,
                f"{site.response_time:.3f}s",
            ])
    return output.getvalue()


def to_markdown(results: list[ScanResult]) -> str:
    """Serialize scan results to Markdown table."""
    lines = ["# VoidLens Scan Report\n"]
    for result in results:
        lines.append(f"## {result.scan_type.value.title()}: `{result.query}`\n")
        lines.append(f"| Site | Category | Status | URL |")
        lines.append(f"|------|----------|--------|-----|")
        for site in result.results:
            lines.append(
                f"| {site.site} | {site.category} | {site.status.value} | {site.url} |"
            )
        lines.append(f"\n**Found:** {result.found_count} | "
                      f"**Not Found:** {result.not_found_count} | "
                      f"**Errors:** {result.error_count} | "
                      f"**Elapsed:** {result.elapsed}s\n")
    return "\n".join(lines)


def to_html(results: list[ScanResult]) -> str:
    """Serialize scan results to a styled HTML report."""
    rows = []
    for result in results:
        for site in result.results:
            status_class = site.status.value.lower().replace(" ", "-")
            rows.append(f"""
                <tr class="{status_class}">
                    <td>{site.site}</td>
                    <td>{site.category}</td>
                    <td class="status">{site.status.value}</td>
                    <td><a href="{site.url}" target="_blank">{site.url}</a></td>
                    <td>{site.reason}</td>
                </tr>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VoidLens Report</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 2rem; }}
  h1 {{ color: #00ff41; text-shadow: 0 0 10px #00ff41; margin-bottom: 1rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th {{ background: #111; color: #00ff41; padding: 0.8rem; text-align: left; border-bottom: 2px solid #00ff41; }}
  td {{ padding: 0.6rem 0.8rem; border-bottom: 1px solid #1a1a1a; }}
  tr:hover {{ background: #111; }}
  a {{ color: #00ccff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .found .status {{ color: #00ff41; font-weight: bold; }}
  .not-found .status {{ color: #555; }}
  .error .status {{ color: #ff4444; }}
  .unknown .status {{ color: #ffaa00; }}
  .registered .status {{ color: #00ff41; font-weight: bold; }}
  .not-registered .status {{ color: #555; }}
</style>
</head>
<body>
<h1>&#x25C8; VoidLens Report</h1>
<table>
<thead><tr><th>Site</th><th>Category</th><th>Status</th><th>URL</th><th>Reason</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>
</body>
</html>"""


def to_xml(results: list[ScanResult]) -> str:
    """Serialize scan results to XML."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<voidlens_report>"]
    for result in results:
        lines.append(f'  <scan query="{result.query}" type="{result.scan_type.value}">')
        for site in result.results:
            lines.append(f"    <result>")
            lines.append(f"      <site>{site.site}</site>")
            lines.append(f"      <status>{site.status.value}</status>")
            lines.append(f"      <url>{site.url}</url>")
            lines.append(f"      <category>{site.category}</category>")
            lines.append(f"      <reason>{site.reason}</reason>")
            lines.append(f"    </result>")
        lines.append("  </scan>")
    lines.append("</voidlens_report>")
    return "\n".join(lines)


def to_sarif(results: list[ScanResult]) -> str:
    """Serialize scan results to SARIF 2.1.0 format for CI integration."""
    sarif: dict[str, Any] = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "VoidLens",
                    "version": "1.0.0",
                    "informationUri": "https://github.com/voidlens/voidlens",
                }
            },
            "results": [],
        }],
    }
    for result in results:
        for site in result.results:
            sarif["runs"][0]["results"].append({
                "ruleId": f"voidlens/{result.scan_type.value}",
                "level": "note",
                "message": {"text": f"{site.site}: {site.status.value}"},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": site.url}
                    }
                }],
            })
    return json.dumps(sarif, indent=2)


def export(
    results: list[ScanResult],
    filepath: str | Path,
    fmt: str = "json",
) -> None:
    """Export results to file in the specified format."""
    formatters = {
        "json": to_json,
        "csv": to_csv,
        "html": to_html,
        "md": to_markdown,
        "xml": to_xml,
        "sarif": to_sarif,
    }
    formatter = formatters.get(fmt)
    if not formatter:
        raise ValueError(f"Unsupported format: {fmt}. Use: {', '.join(formatters)}")

    content = formatter(results)
    Path(filepath).write_text(content, encoding="utf-8")
