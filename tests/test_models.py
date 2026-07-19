"""Tests for core data models."""

from voidlens.constants import Status, ScanType, Category
from voidlens.core.models import SiteResult, ScanResult, ProfileMetadata, ScanSummary


def test_site_result_to_dict():
    result = SiteResult(
        site="GitHub", status=Status.FOUND,
        url="https://github.com/test", category=Category.DEVELOPER,
        reason="exists", response_time=0.5, status_code=200,
    )
    d = result.to_dict()
    assert d["site"] == "GitHub"
    assert d["status"] == "Found"
    assert d["response_time"] == 0.5


def test_site_result_with_metadata():
    meta = ProfileMetadata(display_name="Test User", followers=100)
    result = SiteResult(
        site="GitHub", status=Status.FOUND, url="https://github.com/test",
        category=Category.DEVELOPER, metadata=meta,
    )
    d = result.to_dict()
    assert "metadata" in d
    assert d["metadata"]["display_name"] == "Test User"
    assert d["metadata"]["followers"] == 100


def test_scan_result_counts():
    scan = ScanResult(query="test", scan_type=ScanType.USERNAME)
    scan.results = [
        SiteResult(site="A", status=Status.FOUND),
        SiteResult(site="B", status=Status.FOUND),
        SiteResult(site="C", status=Status.NOT_FOUND),
        SiteResult(site="D", status=Status.ERROR),
        SiteResult(site="E", status=Status.UNKNOWN),
    ]
    assert scan.found_count == 2
    assert scan.not_found_count == 1
    assert scan.error_count == 1
    assert scan.unknown_count == 1


def test_scan_result_to_dict():
    scan = ScanResult(query="johndoe", scan_type=ScanType.USERNAME)
    scan.started_at = 1000.0
    scan.finished_at = 1002.5
    scan.results = [SiteResult(site="GitHub", status=Status.FOUND)]
    d = scan.to_dict()
    assert d["query"] == "johndoe"
    assert d["type"] == "username"
    assert d["elapsed_seconds"] == 2.5
    assert d["found"] == 1


def test_scan_summary_merge():
    summary = ScanSummary()
    scan1 = ScanResult(query="a", scan_type=ScanType.USERNAME)
    scan1.started_at = 0
    scan1.finished_at = 1.0
    scan1.results = [
        SiteResult(site="X", status=Status.FOUND),
        SiteResult(site="Y", status=Status.NOT_FOUND),
    ]
    scan2 = ScanResult(query="b", scan_type=ScanType.EMAIL)
    scan2.started_at = 0
    scan2.finished_at = 0.5
    scan2.results = [SiteResult(site="Z", status=Status.ERROR)]

    summary.merge(scan1)
    summary.merge(scan2)

    assert summary.total_queries == 2
    assert summary.total_sites == 3
    assert summary.total_found == 1
    assert summary.total_not_found == 1
    assert summary.total_errors == 1


def test_profile_metadata_filters_none():
    meta = ProfileMetadata(display_name="Test", bio=None, followers=50)
    d = meta.to_dict()
    assert "bio" not in d
    assert d["display_name"] == "Test"
    assert d["followers"] == 50
