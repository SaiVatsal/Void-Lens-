"""
VoidLens user-agent manager — rotating UA strings and custom headers.

Provides desktop and mobile browser profiles to reduce fingerprinting
during high-volume scans.
"""

from __future__ import annotations

import random

DESKTOP_AGENTS: list[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

MOBILE_AGENTS: list[str] = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]


class UserAgentManager:
    """
    Rotating user-agent provider with desktop/mobile profiles.

    Supports custom header injection and per-request UA rotation.
    """

    def __init__(
        self,
        custom_agents: list[str] | None = None,
        use_mobile: bool = False,
        custom_headers: dict[str, str] | None = None,
    ) -> None:
        self._pool: list[str] = []
        if custom_agents:
            self._pool.extend(custom_agents)
        else:
            self._pool.extend(DESKTOP_AGENTS)
            if use_mobile:
                self._pool.extend(MOBILE_AGENTS)
        self._custom_headers = custom_headers or {}
        self._index = 0

    def get(self) -> str:
        """Return next user-agent string (round-robin with jitter)."""
        agent = self._pool[self._index % len(self._pool)]
        self._index += 1
        return agent

    def get_random(self) -> str:
        """Return a random user-agent string."""
        return random.choice(self._pool)

    def get_headers(self) -> dict[str, str]:
        """Return a complete header dict with rotated UA and custom headers."""
        headers = {
            "User-Agent": self.get(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
        }
        headers.update(self._custom_headers)
        return headers
