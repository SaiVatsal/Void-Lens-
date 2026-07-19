"""Medium — username profile check via page probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.username_scan.base import BaseUsernameModule


class MediumUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Medium", "url": "https://medium.com", "category": Category.BLOGGING}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://medium.com/@{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and username.lower() in body.lower():
                return SiteResult(
                    site="Medium", status=Status.FOUND, url=url,
                    category=Category.BLOGGING, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                )
            if status_code == 404 or status_code == 410:
                return SiteResult(
                    site="Medium", status=Status.NOT_FOUND, url=url,
                    category=Category.BLOGGING, reason="Not found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(site="Medium", status=Status.UNKNOWN, url=url,
                              category=Category.BLOGGING, reason=f"HTTP {status_code}",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Medium", status=Status.ERROR, url=url,
                              category=Category.BLOGGING, reason=str(exc))
