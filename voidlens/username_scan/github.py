"""GitHub — username profile check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class GitHubUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "GitHub", "url": "https://github.com", "category": Category.DEVELOPER}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://api.github.com/users/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                import json
                data = json.loads(body)
                return SiteResult(
                    site="GitHub", status=Status.FOUND,
                    url=f"https://github.com/{username}",
                    category=Category.DEVELOPER, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=data.get("name"),
                        bio=data.get("bio"),
                        avatar_url=data.get("avatar_url"),
                        profile_url=f"https://github.com/{username}",
                        followers=data.get("followers"),
                        following=data.get("following"),
                        repositories=data.get("public_repos"),
                        created_at=data.get("created_at"),
                        extra={"company": data.get("company"), "location": data.get("location")},
                    ),
                )
            if status_code == 404:
                return SiteResult(
                    site="GitHub", status=Status.NOT_FOUND,
                    url=f"https://github.com/{username}",
                    category=Category.DEVELOPER, reason="User not found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="GitHub", status=Status.UNKNOWN,
                url=f"https://github.com/{username}",
                category=Category.DEVELOPER, reason=f"HTTP {status_code}",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="GitHub", status=Status.ERROR, url=f"https://github.com/{username}",
                              category=Category.DEVELOPER, reason=str(exc))
