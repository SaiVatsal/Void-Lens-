"""
VoidLens data models — typed dataclasses for scan results and metadata.

All scan output flows through these models to ensure type-safety and
consistent serialization across export formats.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict
from typing import Any

from voidlens.constants import Status, Category, ScanType


@dataclass(slots=True)
class ProfileMetadata:
    """Publicly available profile metadata collected during a scan."""
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    profile_url: str | None = None
    followers: int | None = None
    following: int | None = None
    posts: int | None = None
    likes: int | None = None
    repositories: int | None = None
    stars: int | None = None
    badges: int | None = None
    country: str | None = None
    verified: bool | None = None
    private: bool | None = None
    created_at: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


@dataclass(slots=True)
class SiteResult:
    """Result from scanning a single site/service."""
    site: str
    status: Status
    url: str = ""
    category: str = Category.SOCIAL
    reason: str = ""
    response_time: float = 0.0
    status_code: int = 0
    metadata: ProfileMetadata = field(default_factory=ProfileMetadata)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "site": self.site,
            "status": self.status.value,
            "url": self.url,
            "category": self.category,
            "reason": self.reason,
            "response_time": round(self.response_time, 3),
            "status_code": self.status_code,
        }
        meta = self.metadata.to_dict()
        if meta:
            d["metadata"] = meta
        return d


@dataclass(slots=True)
class ScanResult:
    """Aggregated result for a complete scan operation."""
    query: str
    scan_type: ScanType
    results: list[SiteResult] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    finished_at: float = 0.0

    @property
    def elapsed(self) -> float:
        return round(self.finished_at - self.started_at, 2)

    @property
    def found_count(self) -> int:
        return sum(
            1 for r in self.results
            if r.status in (Status.FOUND, Status.REGISTERED)
        )

    @property
    def not_found_count(self) -> int:
        return sum(
            1 for r in self.results
            if r.status in (Status.NOT_FOUND, Status.NOT_REGISTERED)
        )

    @property
    def unknown_count(self) -> int:
        return sum(1 for r in self.results if r.status == Status.UNKNOWN)

    @property
    def error_count(self) -> int:
        return sum(1 for r in self.results if r.status == Status.ERROR)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "type": self.scan_type.value,
            "elapsed_seconds": self.elapsed,
            "total": len(self.results),
            "found": self.found_count,
            "not_found": self.not_found_count,
            "unknown": self.unknown_count,
            "errors": self.error_count,
            "results": [r.to_dict() for r in self.results],
        }


@dataclass(slots=True)
class ScanSummary:
    """Summary statistics for a batch of scans."""
    total_queries: int = 0
    total_sites: int = 0
    total_found: int = 0
    total_not_found: int = 0
    total_unknown: int = 0
    total_errors: int = 0
    elapsed_seconds: float = 0.0

    def merge(self, result: ScanResult) -> None:
        self.total_queries += 1
        self.total_sites += len(result.results)
        self.total_found += result.found_count
        self.total_not_found += result.not_found_count
        self.total_unknown += result.unknown_count
        self.total_errors += result.error_count
        self.elapsed_seconds += result.elapsed

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
