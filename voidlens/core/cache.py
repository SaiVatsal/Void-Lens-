"""
VoidLens cache — SQLite-backed result cache with configurable TTL.

Prevents duplicate lookups within the TTL window across scan sessions.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import aiosqlite

from voidlens.constants import DEFAULT_CACHE_TTL


class ScanCache:
    """
    Async SQLite cache for scan results.

    Stores results keyed by (query, site) with a configurable TTL.
    """

    def __init__(
        self,
        db_path: str | Path = "voidlens_cache.db",
        ttl: int = DEFAULT_CACHE_TTL,
    ) -> None:
        self._db_path = str(db_path)
        self._ttl = ttl
        self._db: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        """)
        await self._db.commit()

    async def close(self) -> None:
        if self._db:
            await self._db.close()

    def _make_key(self, query: str, site: str) -> str:
        return f"{query}::{site}"

    async def get(self, query: str, site: str) -> dict | None:
        """Retrieve cached result if within TTL, else None."""
        if not self._db:
            return None
        key = self._make_key(query, site)
        async with self._db.execute(
            "SELECT value, timestamp FROM cache WHERE key = ?", (key,)
        ) as cursor:
            row = await cursor.fetchone()
            if row and (time.time() - row[1]) < self._ttl:
                return json.loads(row[0])
        return None

    async def set(self, query: str, site: str, value: dict) -> None:
        """Store a result in the cache."""
        if not self._db:
            return
        key = self._make_key(query, site)
        await self._db.execute(
            "INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
            (key, json.dumps(value), time.time()),
        )
        await self._db.commit()

    async def clear_expired(self) -> int:
        """Remove expired entries. Returns count of removed rows."""
        if not self._db:
            return 0
        cutoff = time.time() - self._ttl
        cursor = await self._db.execute(
            "DELETE FROM cache WHERE timestamp < ?", (cutoff,)
        )
        await self._db.commit()
        return cursor.rowcount

    async def clear_all(self) -> None:
        """Purge entire cache."""
        if not self._db:
            return
        await self._db.execute("DELETE FROM cache")
        await self._db.commit()
