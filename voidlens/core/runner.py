"""
VoidLens runner — scan orchestrator.

Loads modules, dispatches concurrent scans, aggregates results.
Provides the library-mode API: scan_email() and scan_username().
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Sequence

from voidlens.constants import ScanType, Status
from voidlens.core.engine import ScanEngine
from voidlens.core.models import ScanResult, SiteResult
from voidlens.core.cache import ScanCache
from voidlens.core.proxy import ProxyManager
from voidlens.core.user_agent import UserAgentManager

logger = logging.getLogger("voidlens.runner")


async def _run_module(module, query: str, engine: ScanEngine, cache: ScanCache | None) -> SiteResult:
    """Execute a single module's check with caching and error handling."""
    meta = module.metadata()
    site_name = meta["name"]

    # Check cache
    if cache:
        cached = await cache.get(query, site_name)
        if cached:
            return SiteResult(
                site=cached["site"],
                status=Status(cached["status"]),
                url=cached.get("url", ""),
                category=cached.get("category", ""),
                reason="cached",
            )

    try:
        result = await module.check(query, engine)
        # Cache the result
        if cache:
            await cache.set(query, site_name, result.to_dict())
        return result
    except Exception as exc:
        logger.warning("Module %s failed for %s: %s", site_name, query, exc)
        return SiteResult(
            site=site_name,
            status=Status.ERROR,
            url=meta.get("url", ""),
            category=meta.get("category", ""),
            reason=str(exc),
        )


async def scan_username(
    username: str,
    categories: list[str] | None = None,
    modules: list[str] | None = None,
    concurrency: int = 100,
    timeout: int = 5,
    proxy_file: str | None = None,
    use_cache: bool = True,
) -> ScanResult:
    """
    Scan a username across all registered username modules.

    Library-mode entry point::

        from voidlens import scan_username
        result = await scan_username("johndoe")

    Args:
        username: Username to scan.
        categories: Optional list of categories to filter modules.
        modules: Optional list of specific module names to run.
        concurrency: Max concurrent requests.
        timeout: Request timeout in seconds.
        proxy_file: Path to proxy list file.
        use_cache: Whether to use SQLite cache.

    Returns:
        ScanResult with all site results.
    """
    from voidlens.username_scan import get_all_modules, get_modules_by_category

    scan_result = ScanResult(query=username, scan_type=ScanType.USERNAME)

    # Resolve modules
    all_mods = get_all_modules()
    selected = []

    if modules:
        for name in modules:
            mod = all_mods.get(name.lower())
            if mod:
                selected.append(mod)
    elif categories:
        for cat in categories:
            selected.extend(get_modules_by_category(cat))
    else:
        selected = list(all_mods.values())

    if not selected:
        scan_result.finished_at = time.time()
        return scan_result

    # Setup engine
    proxy_mgr = ProxyManager(proxy_file=proxy_file) if proxy_file else None
    cache = ScanCache() if use_cache else None

    if cache:
        await cache.connect()

    try:
        async with ScanEngine(
            concurrency=concurrency,
            timeout=timeout,
            proxy_manager=proxy_mgr,
        ) as engine:
            tasks = [
                _run_module(mod, username, engine, cache)
                for mod in selected
            ]
            results = await asyncio.gather(*tasks)
            scan_result.results = list(results)
    finally:
        if cache:
            await cache.close()

    scan_result.finished_at = time.time()
    return scan_result


async def scan_email(
    email: str,
    categories: list[str] | None = None,
    modules: list[str] | None = None,
    concurrency: int = 100,
    timeout: int = 5,
    proxy_file: str | None = None,
    use_cache: bool = True,
) -> ScanResult:
    """
    Scan an email across all registered email modules.

    Library-mode entry point::

        from voidlens import scan_email
        result = await scan_email("test@gmail.com")

    Args:
        email: Email address to scan.
        categories: Optional list of categories to filter modules.
        modules: Optional list of specific module names to run.
        concurrency: Max concurrent requests.
        timeout: Request timeout in seconds.
        proxy_file: Path to proxy list file.
        use_cache: Whether to use SQLite cache.

    Returns:
        ScanResult with all site results.
    """
    from voidlens.email_scan import get_all_modules, get_modules_by_category

    scan_result = ScanResult(query=email, scan_type=ScanType.EMAIL)

    # Resolve modules
    all_mods = get_all_modules()
    selected = []

    if modules:
        for name in modules:
            mod = all_mods.get(name.lower())
            if mod:
                selected.append(mod)
    elif categories:
        for cat in categories:
            selected.extend(get_modules_by_category(cat))
    else:
        selected = list(all_mods.values())

    if not selected:
        scan_result.finished_at = time.time()
        return scan_result

    proxy_mgr = ProxyManager(proxy_file=proxy_file) if proxy_file else None
    cache = ScanCache() if use_cache else None

    if cache:
        await cache.connect()

    try:
        async with ScanEngine(
            concurrency=concurrency,
            timeout=timeout,
            proxy_manager=proxy_mgr,
        ) as engine:
            tasks = [
                _run_module(mod, email, engine, cache)
                for mod in selected
            ]
            results = await asyncio.gather(*tasks)
            scan_result.results = list(results)
    finally:
        if cache:
            await cache.close()

    scan_result.finished_at = time.time()
    return scan_result


async def scan_batch(
    queries: Sequence[str],
    scan_type: ScanType,
    **kwargs,
) -> list[ScanResult]:
    """Run scans for multiple queries sequentially."""
    results = []
    scan_fn = scan_username if scan_type == ScanType.USERNAME else scan_email
    for query in queries:
        result = await scan_fn(query, **kwargs)
        results.append(result)
    return results
