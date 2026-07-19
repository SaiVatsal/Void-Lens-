"""
VoidLens username scan base — abstract base class for username intelligence modules.

Every username module must subclass BaseUsernameModule and implement
metadata() and check(). The registry auto-discovers all modules in this package.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from voidlens.core.models import SiteResult

if TYPE_CHECKING:
    from voidlens.core.engine import ScanEngine


class BaseUsernameModule(ABC):
    """
    Abstract base for username intelligence modules.

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
    async def check(self, username: str, engine: ScanEngine) -> SiteResult:
        """
        Check if the given username exists on this service.

        Args:
            username: The username to look up.
            engine: The async HTTP engine for making requests.

        Returns:
            SiteResult with status Found/NotFound/Unknown/Error.
        """
        ...

    def category(self) -> str:
        """Return the category from metadata."""
        return self.metadata().get("category", "Social")

    def supports_bulk(self) -> bool:
        """Whether this module supports batch username checking."""
        return False

    def register(self) -> dict:
        """Return registration info — called by auto-discovery."""
        return self.metadata()
