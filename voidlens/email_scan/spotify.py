"""Spotify — email registration check via signup flow."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class SpotifyEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Spotify", "url": "https://spotify.com", "category": Category.MUSIC}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and '"status":20' in body:
                return SiteResult(
                    site="Spotify", status=Status.REGISTERED, url="https://spotify.com",
                    category=Category.MUSIC, reason="Email already registered",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Spotify", status=Status.NOT_REGISTERED, url="https://spotify.com",
                category=Category.MUSIC, reason="Email not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Spotify", status=Status.ERROR, url="https://spotify.com",
                              category=Category.MUSIC, reason=str(exc))
