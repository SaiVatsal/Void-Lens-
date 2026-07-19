"""GitLab — username profile check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class GitLabUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "GitLab", "url": "https://gitlab.com", "category": Category.DEVELOPER}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://gitlab.com/api/v4/users?username={username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            import json
            if status_code == 200:
                users = json.loads(body)
                if users:
                    u = users[0]
                    return SiteResult(
                        site="GitLab", status=Status.FOUND,
                        url=u.get("web_url", f"https://gitlab.com/{username}"),
                        category=Category.DEVELOPER, reason="Profile exists",
                        response_time=elapsed, status_code=status_code,
                        metadata=ProfileMetadata(
                            display_name=u.get("name"),
                            avatar_url=u.get("avatar_url"),
                            profile_url=u.get("web_url"),
                        ),
                    )
            return SiteResult(
                site="GitLab", status=Status.NOT_FOUND, url=f"https://gitlab.com/{username}",
                category=Category.DEVELOPER, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="GitLab", status=Status.ERROR, url=f"https://gitlab.com/{username}",
                              category=Category.DEVELOPER, reason=str(exc))
