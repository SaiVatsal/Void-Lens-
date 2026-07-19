"""
VoidLens report — summary stats builder for scan results.
"""

from __future__ import annotations

from voidlens.core.models import ScanResult, ScanSummary


def build_summary(results: list[ScanResult]) -> ScanSummary:
    """Aggregate multiple ScanResults into a single ScanSummary."""
    summary = ScanSummary()
    for result in results:
        summary.merge(result)
    return summary
