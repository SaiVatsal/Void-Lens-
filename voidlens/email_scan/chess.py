"""Chess.com — email check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult
from voidlens.email_scan.base import BaseEmailModule


class ChessEmail(BaseEmailModule):
    def metadata(self) -> dict:
        return {"name": "Chess.com", "url": "https://chess.com", "category": Category.GAMING}

    async def check(self, email: str, engine) -> SiteResult:
        url = f"https://www.chess.com/callback/email/available?email={email}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                import json
                data = json.loads(body)
                if not data.get("isAvailable", True):
                    return SiteResult(
                        site="Chess.com", status=Status.REGISTERED, url="https://chess.com",
                        category=Category.GAMING, reason="Email registered",
                        response_time=elapsed, status_code=status_code,
                    )
                return SiteResult(
                    site="Chess.com", status=Status.NOT_REGISTERED, url="https://chess.com",
                    category=Category.GAMING, reason="Email available",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="Chess.com", status=Status.UNKNOWN, url="https://chess.com",
                category=Category.GAMING, reason=f"HTTP {status_code}",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="Chess.com", status=Status.ERROR, url="https://chess.com",
                              category=Category.GAMING, reason=str(exc))
