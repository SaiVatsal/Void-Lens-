"""Twitter/X — username profile check via profile page probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class TwitterUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Twitter", "url": "https://twitter.com", "category": Category.SOCIAL}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://twitter.com/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                return SiteResult(
                    site="Twitter", status=Status.FOUND, url=url,
                    category=Category.SOCIAL, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                )
            if status_code in (404, 302):
                return SiteResult(
                    site="Twitter", status=Status.NOT_FOUND, url=url,
                    category=Category.SOCIAL, reason="Not found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(site="Twitter", status=Status.UNKNOWN, url=url,
                              category=Category.SOCIAL, reason=f"HTTP {status_code}",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Twitter", status=Status.ERROR, url=url,
                              category=Category.SOCIAL, reason=str(exc))
