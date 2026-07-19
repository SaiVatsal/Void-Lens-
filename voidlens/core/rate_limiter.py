"""
VoidLens rate limiter — adaptive per-host concurrency and backoff.

Handles HTTP 429 responses, network timeouts, and exponential backoff
to prevent service blocks during high-concurrency scanning.
"""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class HostState:
    """Tracks rate-limit state for a single host."""
    semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(10))
    backoff_until: float = 0.0
    consecutive_429s: int = 0
    consecutive_errors: int = 0


class RateLimiter:
    """
    Adaptive per-host rate limiter with exponential backoff.

    Features:
        - Per-host concurrency semaphores
        - HTTP 429 detection and automatic cooldown
        - Exponential backoff on repeated failures
        - Network timeout recovery
    """

    def __init__(
        self,
        default_concurrency: int = 10,
        max_backoff: float = 60.0,
        base_delay: float = 1.0,
    ) -> None:
        self._default_concurrency = default_concurrency
        self._max_backoff = max_backoff
        self._base_delay = base_delay
        self._hosts: dict[str, HostState] = defaultdict(
            lambda: HostState(
                semaphore=asyncio.Semaphore(self._default_concurrency)
            )
        )

    def _extract_host(self, url: str) -> str:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.hostname or url

    async def acquire(self, url: str) -> None:
        """Acquire permission to make a request to the given URL's host."""
        host = self._extract_host(url)
        state = self._hosts[host]

        now = time.monotonic()
        if state.backoff_until > now:
            await asyncio.sleep(state.backoff_until - now)

        await state.semaphore.acquire()

    def release(self, url: str) -> None:
        """Release the host semaphore after request completion."""
        host = self._extract_host(url)
        state = self._hosts[host]
        state.semaphore.release()

    def report_success(self, url: str) -> None:
        """Reset error counters on successful request."""
        host = self._extract_host(url)
        state = self._hosts[host]
        state.consecutive_429s = 0
        state.consecutive_errors = 0

    def report_429(self, url: str) -> None:
        """Handle HTTP 429 Too Many Requests — apply exponential backoff."""
        host = self._extract_host(url)
        state = self._hosts[host]
        state.consecutive_429s += 1
        delay = min(
            self._base_delay * (2 ** state.consecutive_429s),
            self._max_backoff,
        )
        state.backoff_until = time.monotonic() + delay

    def report_error(self, url: str) -> None:
        """Handle network errors — apply lighter backoff."""
        host = self._extract_host(url)
        state = self._hosts[host]
        state.consecutive_errors += 1
        if state.consecutive_errors >= 3:
            delay = min(
                self._base_delay * state.consecutive_errors,
                self._max_backoff / 2,
            )
            state.backoff_until = time.monotonic() + delay

    def report_timeout(self, url: str) -> None:
        """Handle request timeout — same as network error."""
        self.report_error(url)
