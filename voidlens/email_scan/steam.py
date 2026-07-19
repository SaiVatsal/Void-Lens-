"""Steam — email registration check via store page probe."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class SteamEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Steam", "url": "https://store.steampowered.com", "category": Category.GAMING}

    async def check(self, email: str, engine) -> SiteResult:
        url = "https://store.steampowered.com/join/ajaxverifyemail"
        try:
            status_code, body, elapsed = await engine.request(
                url, method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=f"email={email}",
            )
            if "avail" in body.lower() or status_code == 200:
                if "success" in body.lower() and "42" not in body:
                    return SiteResult(
                        site="Steam", status=Status.NOT_REGISTERED,
                        url="https://store.steampowered.com", category=Category.GAMING,
                        reason="Email available", response_time=elapsed, status_code=status_code,
                    )
                return SiteResult(
                    site="Steam", status=Status.REGISTERED,
                    url="https://store.steampowered.com", category=Category.GAMING,
                    reason="Email in use", response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Steam", status=Status.UNKNOWN,
                url="https://store.steampowered.com", category=Category.GAMING,
                reason=f"HTTP {status_code}", response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Steam", status=Status.ERROR,
                              url="https://store.steampowered.com", category=Category.GAMING, reason=str(exc))
