"""
VoidLens async engine — core HTTP client with connection pooling and rate limiting.

Provides the low-level async HTTP session used by all scan modules.
Handles retries, timeouts, proxy routing, and rate-limit compliance.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

import aiohttp
from aiohttp import ClientTimeout

from voidlens.constants import DEFAULT_TIMEOUT, DEFAULT_CONCURRENCY, DEFAULT_RETRIES
from voidlens.core.rate_limiter import RateLimiter
from voidlens.core.user_agent import UserAgentManager
from voidlens.core.proxy import ProxyManager


class ScanEngine:
    """
    Async HTTP engine with connection pooling, rate limiting, and retries.

    Usage::

        async with ScanEngine() as engine:
            status, body, elapsed = await engine.request("https://example.com")
    """

    def __init__(
        self,
        concurrency: int = DEFAULT_CONCURRENCY,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        proxy_manager: ProxyManager | None = None,
        user_agent_manager: UserAgentManager | None = None,
    ) -> None:
        self._concurrency = concurrency
        self._timeout = ClientTimeout(total=timeout)
        self._retries = retries
        self._semaphore = asyncio.Semaphore(concurrency)
        self._rate_limiter = RateLimiter(default_concurrency=min(concurrency, 10))
        self._proxy_manager = proxy_manager
        self._ua_manager = user_agent_manager or UserAgentManager()
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> ScanEngine:
        connector = aiohttp.TCPConnector(
            limit=self._concurrency,
            limit_per_host=10,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
        )
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=self._timeout,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def request(
        self,
        url: str,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        allow_redirects: bool = True,
        **kwargs: Any,
    ) -> tuple[int, str, float]:
        """
        Execute an HTTP request with rate limiting, retries, and proxy rotation.

        Returns:
            Tuple of (status_code, response_text, elapsed_seconds).
        """
        assert self._session is not None, "Engine not initialized. Use 'async with'."

        req_headers = self._ua_manager.get_headers()
        if headers:
            req_headers.update(headers)

        proxy_url = None
        if self._proxy_manager:
            proxy_url = self._proxy_manager.get_proxy()

        last_error: Exception | None = None
        for attempt in range(self._retries):
            try:
                await self._rate_limiter.acquire(url)
                async with self._semaphore:
                    start = time.monotonic()
                    async with self._session.request(
                        method,
                        url,
                        headers=req_headers,
                        proxy=proxy_url,
                        allow_redirects=allow_redirects,
                        ssl=False,
                        **kwargs,
                    ) as resp:
                        body = await resp.text(errors="replace")
                        elapsed = time.monotonic() - start

                        if resp.status == 429:
                            self._rate_limiter.report_429(url)
                            if attempt < self._retries - 1:
                                continue
                        else:
                            self._rate_limiter.report_success(url)

                        return resp.status, body, elapsed
            except asyncio.TimeoutError:
                self._rate_limiter.report_timeout(url)
                last_error = asyncio.TimeoutError(f"Timeout: {url}")
            except aiohttp.ClientError as exc:
                self._rate_limiter.report_error(url)
                last_error = exc
            finally:
                self._rate_limiter.release(url)

            if attempt < self._retries - 1:
                await asyncio.sleep(1.0 * (2 ** attempt))

        raise last_error or Exception(f"Request failed: {url}")

    async def head(self, url: str, **kwargs: Any) -> tuple[int, float]:
        """HEAD request — returns (status_code, elapsed)."""
        assert self._session is not None
        headers = self._ua_manager.get_headers()
        try:
            start = time.monotonic()
            async with self._session.head(
                url, headers=headers, ssl=False, allow_redirects=True, **kwargs
            ) as resp:
                return resp.status, time.monotonic() - start
        except Exception:
            return 0, time.monotonic() - start
