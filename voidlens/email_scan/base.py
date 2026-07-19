"""
VoidLens email scan base — abstract base class for email intelligence modules.

Every email module must subclass BaseEmailModule and implement the
metadata() and check() methods. The registry auto-discovers all
modules in this package.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from voidlens.core.models import SiteResult

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from voidlens.core.engine import ScanEngine


class BaseEmailModule(ABC):
    """
    Abstract base for email intelligence modules.

    Subclass contract:
        - metadata()  → dict with 'name', 'url', 'category'
        - check()     → SiteResult with status and optional metadata
    """

    @abstractmethod
    def metadata(self) -> dict:
        """
        Return module metadata.

        Must include:
            name: str       — display name (e.g. "GitHub")
            url: str        — service homepage
            category: str   — category tag from constants.Category
        """
        ...

    @abstractmethod
    async def check(self, email: str, engine: ScanEngine) -> SiteResult:
        """
        Check if the given email is registered on this service.

        Args:
            email: The email address to check.
            engine: The async HTTP engine for making requests.

        Returns:
            SiteResult with status Registered/NotRegistered/Unknown/Error.
        """
        ...

    def category(self) -> str:
        """Return the category from metadata."""
        return self.metadata().get("category", "Social")

    def supports_bulk(self) -> bool:
        """Whether this module supports batch email checking."""
        return False

    def register(self) -> dict:
        """Return registration info — called by auto-discovery."""
        return self.metadata()
