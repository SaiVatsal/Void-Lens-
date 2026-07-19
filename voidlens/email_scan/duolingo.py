"""Duolingo — email check via public profile search."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class DuolingoEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Duolingo", "url": "https://duolingo.com", "category": Category.EDUCATION}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.duolingo.com/2017-06-30/users?email={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and '"users"' in body:
                import json
                data = json.loads(body)
                users = data.get("users", [])
                if users:
                    return SiteResult(
                        site="Duolingo", status=Status.REGISTERED, url="https://duolingo.com",
                        category=Category.EDUCATION, reason="Account found",
                        response_time=elapsed, status_code=status_code,
                    )
            return SiteResult(
                site="Duolingo", status=Status.NOT_REGISTERED, url="https://duolingo.com",
                category=Category.EDUCATION, reason="No account",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Duolingo", status=Status.ERROR, url="https://duolingo.com",
                              category=Category.EDUCATION, reason=str(exc))
