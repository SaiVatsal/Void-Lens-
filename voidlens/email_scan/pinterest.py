"""Pinterest — email check via public suggestion endpoint."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class PinterestEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Pinterest", "url": "https://pinterest.com", "category": Category.SOCIAL}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.pinterest.com/resource/EmailExistsResource/get/?data=%7B%22options%22%3A%7B%22email%22%3A%22{email}%22%7D%7D"
        try:
            status_code, body, elapsed = await engine.request(url)
            if "true" in body.lower() and status_code == 200:
                return SiteResult(
                    site="Pinterest", status=Status.REGISTERED, url="https://pinterest.com",
                    category=Category.SOCIAL, reason="Email exists",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Pinterest", status=Status.NOT_REGISTERED, url="https://pinterest.com",
                category=Category.SOCIAL, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Pinterest", status=Status.ERROR, url="https://pinterest.com",
                              category=Category.SOCIAL, reason=str(exc))
