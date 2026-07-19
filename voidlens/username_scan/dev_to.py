"""DEV.to — username profile check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class DevToUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "DEV.to", "url": "https://dev.to", "category": Category.DEVELOPER}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://dev.to/api/users/by_username?url={username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                import json
                data = json.loads(body)
                return SiteResult(
                    site="DEV.to", status=Status.FOUND,
                    url=f"https://dev.to/{username}",
                    category=Category.DEVELOPER, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=data.get("name"),
                        bio=data.get("summary"),
                        profile_url=f"https://dev.to/{username}",
                        avatar_url=data.get("profile_image"),
                        created_at=data.get("joined_at"),
                    ),
                )
            return SiteResult(
                site="DEV.to", status=Status.NOT_FOUND, url=f"https://dev.to/{username}",
                category=Category.DEVELOPER, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="DEV.to", status=Status.ERROR, url=f"https://dev.to/{username}",
                              category=Category.DEVELOPER, reason=str(exc))
