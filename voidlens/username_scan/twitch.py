"""Twitch — username profile check via page probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class TwitchUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Twitch", "url": "https://twitch.tv", "category": Category.STREAMING}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://www.twitch.tv/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "isLiveBroadcast" in body or "channelName" in body.lower():
                return SiteResult(site="Twitch", status=Status.FOUND, url=url,
                                  category=Category.STREAMING, reason="Channel exists",
                                  response_time=elapsed, status_code=status_code)
            if status_code == 404 or ("sorry" in body.lower() and "page" in body.lower()):
                return SiteResult(site="Twitch", status=Status.NOT_FOUND, url=url,
                                  category=Category.STREAMING, reason="Not found",
                                  response_time=elapsed, status_code=status_code)
            return SiteResult(site="Twitch", status=Status.UNKNOWN, url=url,
                              category=Category.STREAMING, reason=f"HTTP {status_code}",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Twitch", status=Status.ERROR, url=url,
                              category=Category.STREAMING, reason=str(exc))
