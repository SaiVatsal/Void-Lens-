"""Reddit — username profile check via public JSON API."""

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class RedditUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {"name": "Reddit", "url": "https://reddit.com", "category": Category.FORUMS}

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://www.reddit.com/user/{username}/about.json"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200 and '"kind": "t2"' in body:
                import json
                data = json.loads(body).get("data", {})
                return SiteResult(
                    site="Reddit", status=Status.FOUND,
                    url=f"https://reddit.com/user/{username}",
                    category=Category.FORUMS, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                    metadata=ProfileMetadata(
                        display_name=data.get("subreddit", {}).get("title"),
                        profile_url=f"https://reddit.com/user/{username}",
                        avatar_url=data.get("icon_img"),
                        verified=data.get("verified", False),
                        created_at=str(data.get("created_utc", "")),
                        extra={"comment_karma": data.get("comment_karma"), "link_karma": data.get("link_karma")},
                    ),
                )
            if status_code == 404:
                return SiteResult(
                    site="Reddit", status=Status.NOT_FOUND,
                    url=f"https://reddit.com/user/{username}",
                    category=Category.FORUMS, reason="User not found",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(site="Reddit", status=Status.UNKNOWN, url=f"https://reddit.com/user/{username}",
                              category=Category.FORUMS, reason=f"HTTP {status_code}",
                              response_time=elapsed, status_code=status_code)
        except Exception as exc:
            return SiteResult(site="Reddit", status=Status.ERROR, url=f"https://reddit.com/user/{username}",
                              category=Category.FORUMS, reason=str(exc))
