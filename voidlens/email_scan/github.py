"""GitHub — email registration check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.email_scan.base import BaseEmailModule


class GitHubEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "GitHub", "url": "https://github.com", "category": Category.DEVELOPER}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://api.github.com/search/users?q={email}+in:email"
        try:
            status_code, body, elapsed = await engine.request(url)
            import json
            data = json.loads(body)
            if data.get("total_count", 0) > 0:
                user = data["items"][0]
                return SiteResult(
                    site="GitHub", status=Status.REGISTERED,
                    url=user.get("html_url", ""), category=Category.DEVELOPER,
                    reason="Email found in public profile", response_time=elapsed,
                    status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=user.get("login"),
                        avatar_url=user.get("avatar_url"),
                        profile_url=user.get("html_url"),
                    ),
                )
            return SiteResult(
                site="GitHub", status=Status.NOT_REGISTERED, url="https://github.com",
                category=Category.DEVELOPER, reason="No public match",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(
                site="GitHub", status=Status.ERROR, url="https://github.com",
                category=Category.DEVELOPER, reason=str(exc),
            )
