"""Spotify — username profile check via open.spotify."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class SpotifyUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Spotify", "url": "https://spotify.com", "category": Category.MUSIC}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://open.spotify.com/user/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "spotify" in body.lower():
                return SiteResult(site="Spotify", status=Status.FOUND, url=url,
                                  category=Category.MUSIC, reason="Profile exists",
                                  response_time=elapsed, status_code=status_code)
            return SiteResult(site="Spotify", status=Status.NOT_FOUND, url=url,
                              category=Category.MUSIC, reason="Not found",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Spotify", status=Status.ERROR, url=url,
                              category=Category.MUSIC, reason=str(exc))
