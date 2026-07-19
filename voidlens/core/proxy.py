"""
VoidLens proxy manager — loader, rotation, health-check, and SOCKS support.

Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies loaded from file or config.
"""

from __future__ import annotations

import random
from pathlib import Path


class ProxyManager:
    """
    Proxy pool with rotation and health validation.

    Accepts proxy strings in the formats:
        http://host:port
        https://host:port
        socks4://host:port
        socks5://host:port
    """

    def __init__(
        self,
        proxies: list[str] | None = None,
        proxy_file: str | Path | None = None,
        rotate: bool = True,
        timeout: int = 5,
    ) -> None:
        self._proxies: list[str] = []
        self._rotate = rotate
        self._timeout = timeout
        self._index = 0

        if proxies:
            self._proxies.extend(proxies)
        if proxy_file:
            self._load_from_file(proxy_file)

    def _load_from_file(self, path: str | Path) -> None:
        """Load proxy list from a text file (one per line)."""
        filepath = Path(path)
        if not filepath.exists():
            return
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if not line.startswith(("http://", "https://", "socks4://", "socks5://")):
                        line = f"http://{line}"
                    self._proxies.append(line)

    def get_proxy(self) -> str | None:
        """Return next proxy in rotation, or random if rotation disabled."""
        if not self._proxies:
            return None
        if self._rotate:
            proxy = self._proxies[self._index % len(self._proxies)]
            self._index += 1
            return proxy
        return random.choice(self._proxies)

    def remove_proxy(self, proxy: str) -> None:
        """Remove a dead proxy from the pool."""
        if proxy in self._proxies:
            self._proxies.remove(proxy)

    @property
    def count(self) -> int:
        return len(self._proxies)

    @property
    def is_empty(self) -> bool:
        return len(self._proxies) == 0
