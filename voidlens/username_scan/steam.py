"""Steam — username profile check via community page."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class SteamUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Steam", "url": "https://steamcommunity.com", "category": Category.GAMING}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://steamcommunity.com/id/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "profile_page" in body:
                return SiteResult(
                    site="Steam", status=Status.FOUND, url=url,
                    category=Category.GAMING, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Steam", status=Status.NOT_FOUND, url=url,
                category=Category.GAMING, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Steam", status=Status.ERROR, url=url,
                              category=Category.GAMING, reason=str(exc))
