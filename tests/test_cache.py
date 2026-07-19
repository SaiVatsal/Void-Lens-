"""Tests for cache module."""

import pytest
import os
from voidlens.core.cache import ScanCache


@pytest.mark.asyncio
async def test_cache_set_and_get(tmp_path):
    db_path = tmp_path / "test_cache.db"
    cache = ScanCache(db_path=str(db_path), ttl=3600)
    await cache.connect()

    await cache.set("user1", "GitHub", {"site": "GitHub", "status": "Found"})
    result = await cache.get("user1", "GitHub")
    assert result is not None
    assert result["site"] == "GitHub"
    assert result["status"] == "Found"

    await cache.close()


@pytest.mark.asyncio
async def test_cache_miss(tmp_path):
    db_path = tmp_path / "test_cache2.db"
    cache = ScanCache(db_path=str(db_path), ttl=3600)
    await cache.connect()

    result = await cache.get("nonexistent", "Nowhere")
    assert result is None

    await cache.close()


@pytest.mark.asyncio
async def test_cache_clear(tmp_path):
    db_path = tmp_path / "test_cache3.db"
    cache = ScanCache(db_path=str(db_path), ttl=3600)
    await cache.connect()

    await cache.set("user1", "GitHub", {"status": "Found"})
    await cache.clear_all()
    result = await cache.get("user1", "GitHub")
    assert result is None

    await cache.close()
