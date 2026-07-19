"""Pinterest — username profile check."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class PinterestUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Pinterest", "url": "https://pinterest.com", "category": Category.SOCIAL}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://www.pinterest.com/{username}/"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "pinterestapp" in body.lower():
                return SiteResult(site="Pinterest", status=Status.FOUND, url=url,
                                  category=Category.SOCIAL, reason="Profile exists",
                                  response_time=elapsed, status_code=status_code)
            return SiteResult(site="Pinterest", status=Status.NOT_FOUND, url=url,
                              category=Category.SOCIAL, reason="Not found",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Pinterest", status=Status.ERROR, url=url,
                              category=Category.SOCIAL, reason=str(exc))
