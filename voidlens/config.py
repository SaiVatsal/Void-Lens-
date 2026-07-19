"""
VoidLens config — YAML configuration loader.

Loads settings from config/config.yaml with sensible defaults.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from voidlens.constants import DEFAULT_TIMEOUT, DEFAULT_CONCURRENCY, DEFAULT_RETRIES


@dataclass
class ProxyConfig:
    enabled: bool = False
    file: str = "config/proxies.yaml"
    rotate: bool = True
    timeout: int = 5


@dataclass
class Config:
    """Application configuration with defaults."""
    timeout: int = DEFAULT_TIMEOUT
    concurrency: int = DEFAULT_CONCURRENCY
    retries: int = DEFAULT_RETRIES
    retry_delay: float = 1.0
    cache_enabled: bool = True
    cache_ttl: int = 3600
    user_agent: str = ""
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    categories: list[str] = field(default_factory=list)
    log_dir: str = "logs"
    verbose: bool = False

    @classmethod
    def load(cls, path: str | Path = "config/config.yaml") -> Config:
        """Load config from YAML file, falling back to defaults."""
        filepath = Path(path)
        if not filepath.exists():
            return cls()

        with open(filepath, "r", encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}

        proxy_data = data.get("proxy", {})
        proxy_cfg = ProxyConfig(
            enabled=proxy_data.get("enabled", False),
            file=proxy_data.get("file", "config/proxies.yaml"),
            rotate=proxy_data.get("rotate", True),
            timeout=proxy_data.get("timeout", 5),
        )

        return cls(
            timeout=data.get("timeout", DEFAULT_TIMEOUT),
            concurrency=data.get("concurrency", DEFAULT_CONCURRENCY),
            retries=data.get("retries", DEFAULT_RETRIES),
            retry_delay=data.get("retry_delay", 1.0),
            cache_enabled=data.get("cache_enabled", True),
            cache_ttl=data.get("cache_ttl", 3600),
            user_agent=data.get("user_agent", ""),
            proxy=proxy_cfg,
            categories=data.get("categories", []),
            log_dir=data.get("log_dir", "logs"),
            verbose=data.get("verbose", False),
        )
