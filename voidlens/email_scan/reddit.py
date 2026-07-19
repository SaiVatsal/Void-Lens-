"""Reddit — email check via public availability endpoint."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class RedditEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Reddit", "url": "https://reddit.com", "category": Category.FORUMS}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.reddit.com/api/check_email.json?email={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                if "true" in body.lower():
                    return SiteResult(
                        site="Reddit", status=Status.REGISTERED, url="https://reddit.com",
                        category=Category.FORUMS, reason="Email in use",
                        response_time=elapsed, status_code=status_code,
                    )
                return SiteResult(
                    site="Reddit", status=Status.NOT_REGISTERED, url="https://reddit.com",
                    category=Category.FORUMS, reason="Email available",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Reddit", status=Status.UNKNOWN, url="https://reddit.com",
                category=Category.FORUMS, reason=f"HTTP {status_code}",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Reddit", status=Status.ERROR, url="https://reddit.com",
                              category=Category.FORUMS, reason=str(exc))
