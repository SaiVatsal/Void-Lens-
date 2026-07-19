"""GitLab — email check via public user search."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class GitLabEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "GitLab", "url": "https://gitlab.com", "category": Category.DEVELOPER}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://gitlab.com/api/v4/users?search={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            import json
            if status_code == 200:
                users = json.loads(body)
                if users:
                    user = users[0]
                    return SiteResult(
                        site="GitLab", status=Status.REGISTERED,
                        url=user.get("web_url", "https://gitlab.com"),
                        category=Category.DEVELOPER, reason="User found",
                        response_time=elapsed, status_code=status_code,
                    )
            return SiteResult(
                site="GitLab", status=Status.NOT_REGISTERED, url="https://gitlab.com",
                category=Category.DEVELOPER, reason="No match",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="GitLab", status=Status.ERROR, url="https://gitlab.com",
                              category=Category.DEVELOPER, reason=str(exc))
