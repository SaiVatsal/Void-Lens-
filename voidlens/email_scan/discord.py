"""Discord — email check via public API probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class DiscordEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Discord", "url": "https://discord.com", "category": Category.SOCIAL}

    async def check(self, email: str, engine) -> SiteResult:
        url = "https://discord.com/api/v9/auth/register"
        try:
            import json
            payload = json.dumps({
                "email": email, "username": "voidlens_probe",
                "password": "Pr0b3T3st!!", "date_of_birth": "1990-01-01",
            })
            status_code, body, elapsed = await engine.request(
                url, method="POST",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            if "EMAIL_ALREADY_REGISTERED" in body or "email" in body.lower():
                return SiteResult(
                    site="Discord", status=Status.REGISTERED, url="https://discord.com",
                    category=Category.SOCIAL, reason="Email registered",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Discord", status=Status.UNKNOWN, url="https://discord.com",
                category=Category.SOCIAL, reason="Unable to determine",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Discord", status=Status.ERROR, url="https://discord.com",
                              category=Category.SOCIAL, reason=str(exc))
