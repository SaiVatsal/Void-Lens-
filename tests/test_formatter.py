"""Tests for formatters."""

from voidlens.constants import Status, ScanType, Category
from voidlens.core.models import SiteResult, ScanResult
from voidlens.core.formatter import to_json, to_csv, to_markdown, to_html, to_xml, to_sarif


def _make_result() -> ScanResult:
    scan = ScanResult(query="testuser", scan_type=ScanType.USERNAME)
    scan.started_at = 1000.0
    scan.finished_at = 1001.0
    scan.results = [
        SiteResult(site="GitHub", status=Status.FOUND, url="https://github.com/testuser",
                   category=Category.DEVELOPER, reason="exists"),
        SiteResult(site="Reddit", status=Status.NOT_FOUND, url="",
                   category=Category.FORUMS, reason="404"),
    ]
    return scan


def test_json_format():
    data = to_json([_make_result()])
    assert '"GitHub"' in data
    assert '"Found"' in data


def test_csv_format():
    data = to_csv([_make_result()])
    assert "GitHub" in data
    assert "Found" in data
    assert "testuser" in data


def test_markdown_format():
    data = to_markdown([_make_result()])
    assert "# VoidLens Scan Report" in data
    assert "GitHub" in data


def test_html_format():
    data = to_html([_make_result()])
    assert "<!DOCTYPE html>" in data
    assert "VoidLens" in data
    assert "#00ff41" in data


def test_xml_format():
    data = to_xml([_make_result()])
    assert '<?xml version="1.0"' in data
    assert "<site>GitHub</site>" in data


def test_sarif_format():
    data = to_sarif([_make_result()])
    assert "sarif-schema-2.1.0" in data
    assert "VoidLens" in data
