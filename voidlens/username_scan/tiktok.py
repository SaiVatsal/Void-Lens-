"""TikTok — username profile check via page probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class TikTokUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "TikTok", "url": "https://tiktok.com", "category": Category.VIDEO}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://www.tiktok.com/@{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "uniqueId" in body:
                return SiteResult(
                    site="TikTok", status=Status.FOUND, url=url,
                    category=Category.VIDEO, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                )
            if status_code == 404 or "couldn" in body.lower():
                return SiteResult(
                    site="TikTok", status=Status.NOT_FOUND, url=url,
                    category=Category.VIDEO, reason="Not found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(site="TikTok", status=Status.UNKNOWN, url=url,
                              category=Category.VIDEO, reason=f"HTTP {status_code}",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="TikTok", status=Status.ERROR, url=url,
                              category=Category.VIDEO, reason=str(exc))
