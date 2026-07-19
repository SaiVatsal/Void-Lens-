# Plugin Guide

## Adding a New Username Module

1. Create a new file in `voidlens/username_scan/`:

```python
# voidlens/username_scan/myservice.py

from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult, ProfileMetadata
from voidlens.username_scan.base import BaseUsernameModule


class MyServiceUsername(BaseUsernameModule):
    def metadata(self) -> dict:
        return {
            "name": "MyService",
            "url": "https://myservice.com",
            "category": Category.SOCIAL,
        }

    async def check(self, username: str, engine) -> SiteResult:
        url = f"https://myservice.com/user/{username}"
        try:
            status_code, body, elapsed = await engine.request(url)
            if status_code == 200:
                return SiteResult(
                    site="MyService", status=Status.FOUND, url=url,
                    category=Category.SOCIAL, reason="Profile exists",
                    response_time=elapsed, status_code=status_code,
                )
            return SiteResult(
                site="MyService", status=Status.NOT_FOUND, url=url,
                category=Category.SOCIAL, reason="Not found",
                response_time=elapsed, status_code=status_code,
            )
        except Exception as exc:
            return SiteResult(
                site="MyService", status=Status.ERROR, url=url,
                category=Category.SOCIAL, reason=str(exc),
            )
```

2. **That's it.** The module auto-registers on next scan.

## Adding a New Email Module

Same pattern — create a file in `voidlens/email_scan/` subclassing `BaseEmailModule`.

## Plugin Contract

Every module must implement:

| Method | Returns | Purpose |
|--------|---------|---------|
| `metadata()` | `dict` | name, url, category |
| `check(query, engine)` | `SiteResult` | Scan logic |

Optional overrides:

| Method | Default | Purpose |
|--------|---------|---------|
| `category()` | From metadata | Category string |
| `supports_bulk()` | `False` | Batch support flag |
| `register()` | Returns metadata | Registration hook |
