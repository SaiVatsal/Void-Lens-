"""Replit — email check via signup validation."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class ReplitEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Replit", "url": "https://replit.com", "category": Category.DEVELOPER}

    async def check(self, email: str, engine) -> SiteResult:
        url = "https://replit.com/signup"
        try:
            status_code, body, elapsed = await engine.request(url)
            return SiteResult(
                site="Replit", status=Status.UNKNOWN, url="https://replit.com",
                category=Category.DEVELOPER, reason="Endpoint requires browser interaction",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Replit", status=Status.ERROR, url="https://replit.com",
                              category=Category.DEVELOPER, reason=str(exc))
