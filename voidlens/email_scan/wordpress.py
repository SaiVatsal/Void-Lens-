"""WordPress — email check via login reset probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class WordPressEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "WordPress", "url": "https://wordpress.com", "category": Category.BLOGGING}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://public-api.wordpress.com/rest/v1.1/users/{email}/auth-options"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and "passwordless" in body:
                return SiteResult(
                    site="WordPress", status=Status.REGISTERED, url="https://wordpress.com",
                    category=Category.BLOGGING, reason="Account exists",
                    response_time=elapsed, status_code=status_code,
                )
            if status_code == 404:
                return SiteResult(
                    site="WordPress", status=Status.NOT_REGISTERED, url="https://wordpress.com",
                    category=Category.BLOGGING, reason="No account",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="WordPress", status=Status.UNKNOWN, url="https://wordpress.com",
                category=Category.BLOGGING, reason=f"HTTP {status_code}",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="WordPress", status=Status.ERROR, url="https://wordpress.com",
                              category=Category.BLOGGING, reason=str(exc))
