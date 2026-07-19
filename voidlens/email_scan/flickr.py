"""Flickr — email check via public people search."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class FlickrEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Flickr", "url": "https://flickr.com", "category": Category.PHOTOGRAPHY}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.flickr.com/people/{email.split('@')[0]}/"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                return SiteResult(
                    site="Flickr", status=Status.REGISTERED, url=url,
                    category=Category.PHOTOGRAPHY, reason="Profile found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Flickr", status=Status.NOT_REGISTERED, url="https://flickr.com",
                category=Category.PHOTOGRAPHY, reason="No profile",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Flickr", status=Status.ERROR, url="https://flickr.com",
                              category=Category.PHOTOGRAPHY, reason=str(exc))
