"""Gravatar — email check via avatar hash lookup."""

import hashlib
from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.email_scan.base import BaseEmailModule


class GravatarEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Gravatar", "url": "https://gravatar.com", "category": Category.SOCIAL}

    async def check(self, email: str, engine) -> SiteResult:
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f"https://en.gravatar.com/{email_hash}.json"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                import json
                data = json.loads(body)
                entry = data.get("entry", [{}])[0]
                return SiteResult(
                    site="Gravatar", status=Status.REGISTERED, url=f"https://gravatar.com/{email_hash}",
                    category=Category.SOCIAL, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=entry.get("displayName"),
                        avatar_url=entry.get("thumbnailUrl"),
                        profile_url=f"https://gravatar.com/{email_hash}",
                    ),
                )
            return SiteResult(
                site="Gravatar", status=Status.NOT_REGISTERED, url="https://gravatar.com",
                category=Category.SOCIAL, reason="No profile", response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Gravatar", status=Status.ERROR, url="https://gravatar.com",
                              category=Category.SOCIAL, reason=str(exc))
