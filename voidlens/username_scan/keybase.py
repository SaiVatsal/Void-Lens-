"""Keybase — username profile check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class KeybaseUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Keybase", "url": "https://keybase.io", "category": Category.SECURITY}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                import json
                data = json.loads(body)
                them = data.get("them", [])
                if them and them[0]:
                    user = them[0]
                    return SiteResult(
                        site="Keybase", status=Status.FOUND,
                        url=f"https://keybase.io/{username}",
                        category=Category.SECURITY, reason="Profile exists",
                        response_time=elapsed, status_code=status_code,
                        metadata=ProfileMetadata(
                            display_name=user.get("profile", {}).get("full_name"),
                            bio=user.get("profile", {}).get("bio"),
                            profile_url=f"https://keybase.io/{username}",
                        ),
                    )
            return SiteResult(
                site="Keybase", status=Status.NOT_FOUND, url=f"https://keybase.io/{username}",
                category=Category.SECURITY, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Keybase", status=Status.ERROR, url=f"https://keybase.io/{username}",
                              category=Category.SECURITY, reason=str(exc))
