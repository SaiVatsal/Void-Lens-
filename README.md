<p align="center">
  <h1 align="center">◈ VoidLens</h1>
  <p align="center"><em>Peer into the digital void.</em></p>
  <p align="center">
    <a href="#installation"><img src="https://img.shields.io/badge/python-3.10+-brightgreen?style=flat-square&logo=python" alt="Python"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"></a>
    <a href="#"><img src="https://img.shields.io/badge/platform-win%20|%20mac%20|%20linux-brightgreen?style=flat-square" alt="Platform"></a>
    <a href="#"><img src="https://img.shields.io/badge/modules-30+-brightgreen?style=flat-square" alt="Modules"></a>
  </p>
</p>

---

A professional **2-in-1 OSINT & Digital Footprint Intelligence Suite** for legitimate cybersecurity reconnaissance, digital footprint auditing, and security awareness.

```
 ██╗   ██╗ ██████╗ ██╗██████╗ ██╗     ███████╗███╗   ██╗███████╗
 ██║   ██║██╔═══██╗██║██╔══██╗██║     ██╔════╝████╗  ██║██╔════╝
 ██║   ██║██║   ██║██║██║  ██║██║     █████╗  ██╔██╗ ██║███████╗
 ╚██╗ ██╔╝██║   ██║██║██║  ██║██║     ██╔══╝  ██║╚██╗██║╚════██║
  ╚████╔╝ ╚██████╔╝██║██████╔╝███████╗███████╗██║ ╚████║███████║
   ╚═══╝   ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
```

## Features

- **Email Intelligence** — Check if an email is registered across 15+ services
- **Username Intelligence** — Scan usernames across 15+ platforms with metadata extraction
- **Async Engine** — aiohttp with connection pooling, adaptive rate limiting, retries
- **Plugin Architecture** — Drop-in modules, zero engine changes
- **Export** — JSON, CSV, HTML, Markdown, XML, SARIF
- **Proxy Support** — HTTP, HTTPS, SOCKS4, SOCKS5 with rotation
- **SQLite Cache** — Prevent duplicate lookups with configurable TTL
- **API Mode** — FastAPI REST endpoints
- **Library Mode** — Importable async functions
- **Docker** — Ready to deploy

## Installation

```bash
pip install -e .
```

With API support:
```bash
pip install -e ".[api]"
```

Full development:
```bash
pip install -e ".[all]"
```

## Quick Start

### CLI

```bash
# Scan a username
voidlens scan -u johndoe

# Scan an email
voidlens scan -e test@gmail.com

# Both at once
voidlens scan -u johndoe -e test@gmail.com

# Bulk scan from file
voidlens scan -uf usernames.txt

# Filter by category
voidlens scan -u johndoe -c developer -c gaming

# Verbose output + export
voidlens scan -u johndoe -v --json report.json --html report.html

# With proxy rotation
voidlens scan -u johndoe -P proxies.txt
```

### Library Mode

```python
import asyncio
from voidlens import scan_username, scan_email

async def main():
    result = await scan_username("johndoe")
    for site in result.results:
        print(f"{site.site}: {site.status.value}")

asyncio.run(main())
```

### API Mode

```bash
uvicorn voidlens.api:app --host 0.0.0.0 --port 8000
```

```bash
curl -X POST http://localhost:8000/scan/username \
  -H "Content-Type: application/json" \
  -d '{"query": "johndoe"}'
```

## Modules

### Email (15)
GitHub, Gravatar, Spotify, Discord, Reddit, Steam, Pinterest, Twitter, Duolingo, Chess.com, GitLab, Replit, WordPress, Tumblr, Flickr

### Username (15)
GitHub, Reddit, Twitter, Instagram, TikTok, Steam, GitLab, Medium, DEV.to, Hacker News, Pinterest, Twitch, SoundCloud, Spotify, Keybase

## Adding a Module

Create a file in `voidlens/username_scan/` or `voidlens/email_scan/`:

```python
from voidlens.username_scan.base import BaseUsernameModule
from voidlens.constants import Status, Category
from voidlens.core.models import SiteResult

class MyServiceUsername(BaseUsernameModule):
    def metadata(self):
        return {"name": "MyService", "url": "https://myservice.com", "category": Category.SOCIAL}

    async def check(self, username, engine):
        status_code, body, elapsed = await engine.request(f"https://myservice.com/{username}")
        status = Status.FOUND if status_code == 200 else Status.NOT_FOUND
        return SiteResult(site="MyService", status=status, url=f"https://myservice.com/{username}",
                          category=Category.SOCIAL, response_time=elapsed, status_code=status_code)
```

Done. Auto-discovered on next scan.

## Project Structure

```
voidlens/
├── __init__.py           # Library exports
├── cli.py                # Typer + Rich CLI
├── api.py                # FastAPI endpoints
├── config.py             # YAML config loader
├── constants.py          # Enums, theme, defaults
├── core/
│   ├── engine.py         # Async HTTP engine
│   ├── runner.py         # Scan orchestrator
│   ├── models.py         # Typed dataclasses
│   ├── rate_limiter.py   # Adaptive rate limiting
│   ├── user_agent.py     # UA rotation
│   ├── proxy.py          # Proxy management
│   ├── cache.py          # SQLite cache
│   ├── formatter.py      # Export formats
│   ├── logger.py         # Rotating file logger
│   └── report.py         # Summary stats
├── email_scan/           # Email modules
├── username_scan/        # Username modules
└── utils/                # Validators, patterns
```

## Documentation

- [Architecture](docs/Architecture.md)
- [Plugin Guide](docs/PluginGuide.md)
- [API Reference](docs/API.md)
- [CLI Reference](docs/CLI.md)
- [Contributing](docs/Contributing.md)

## Legal

This tool is intended for **legitimate** defensive security, OSINT research, digital footprint auditing, bug bounty reconnaissance, and security awareness. It operates within applicable laws, platform terms of service, and ethical guidelines. It does not attempt authentication bypasses, CAPTCHA bypasses, or other techniques intended to evade service protections.

## License

MIT — see [LICENSE](LICENSE)
