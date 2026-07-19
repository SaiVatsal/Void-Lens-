"""Twitter/X — email check via public signup validation."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class TwitterEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Twitter", "url": "https://twitter.com", "category": Category.SOCIAL}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            import json
            data = json.loads(body)
            if data.get("taken", False):
                return SiteResult(
                    site="Twitter", status=Status.REGISTERED, url="https://twitter.com",
                    category=Category.SOCIAL, reason="Email taken",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Twitter", status=Status.NOT_REGISTERED, url="https://twitter.com",
                category=Category.SOCIAL, reason="Email available",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Twitter", status=Status.UNKNOWN, url="https://twitter.com",
                              category=Category.SOCIAL, reason=str(exc))
