"""SoundCloud — username profile check."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class SoundCloudUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "SoundCloud", "url": "https://soundcloud.com", "category": Category.MUSIC}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://soundcloud.com/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "soundcloud" in body.lower():
                return SiteResult(site="SoundCloud", status=Status.FOUND, url=url,
                                  category=Category.MUSIC, reason="Profile exists",
                                  response_time=elapsed, status_code=status_code)
            return SiteResult(site="SoundCloud", status=Status.NOT_FOUND, url=url,
                              category=Category.MUSIC, reason="Not found",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="SoundCloud", status=Status.ERROR, url=url,
                              category=Category.MUSIC, reason=str(exc))
