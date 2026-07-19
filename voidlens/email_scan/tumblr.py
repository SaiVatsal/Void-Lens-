"""Tumblr — email check via public recover page."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class TumblrEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Tumblr", "url": "https://tumblr.com", "category": Category.BLOGGING}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.tumblr.com/api/v2/user/search?q={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "response" in body:
                return SiteResult(
                    site="Tumblr", status=Status.UNKNOWN, url="https://tumblr.com",
                    category=Category.BLOGGING, reason="Search returned results",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Tumblr", status=Status.NOT_REGISTERED, url="https://tumblr.com",
                category=Category.BLOGGING, reason="No results",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Tumblr", status=Status.ERROR, url="https://tumblr.com",
                              category=Category.BLOGGING, reason=str(exc))
