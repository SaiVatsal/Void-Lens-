"""Hacker News — username profile check via public API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class HackerNewsUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "HackerNews", "url": "https://news.ycombinator.com", "category": Category.FORUMS}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and body.strip() != "null":
                import json
                data = json.loads(body)
                return SiteResult(
                    site="HackerNews", status=Status.FOUND,
                    url=f"https://news.ycombinator.com/user?id={username}",
                    category=Category.FORUMS, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=data.get("id"),
                        bio=data.get("about"),
                        extra={"karma": data.get("karma")},
                        created_at=str(data.get("created", "")),
                    ),
                )
            return SiteResult(
                site="HackerNews", status=Status.NOT_FOUND,
                url=f"https://news.ycombinator.com/user?id={username}",
                category=Category.FORUMS, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(site="HackerNews", status=Status.ERROR,
                              url=f"https://news.ycombinator.com/user?id={username}",
                              category=Category.FORUMS, reason=str(exc))
