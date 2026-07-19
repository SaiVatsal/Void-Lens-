"""
VoidLens constants — status enums, categories, defaults, theme colors.

Centralizes all magic strings and configuration defaults used across the framework.
"""

from enum import Enum


class Status(str, Enum):
    """Scan result status codes."""
    FOUND = "Found"
    NOT_FOUND = "Not Found"
    REGISTERED = "Registered"
    NOT_REGISTERED = "Not Registered"
    UNKNOWN = "Unknown"
    ERROR = "Error"


class Category(str, Enum):
    """Platform category tags."""
    DEVELOPER = "Developer"
    SOCIAL = "Social"
    FORUMS = "Forums"
    STREAMING = "Streaming"
    GAMING = "Gaming"
    SHOPPING = "Shopping"
    PROGRAMMING = "Programming"
    FINANCE = "Finance"
    CLOUD = "Cloud"
    MUSIC = "Music"
    EDUCATION = "Education"
    PRODUCTIVITY = "Productivity"
    SECURITY = "Security"
    OPEN_SOURCE = "Open Source"
    AI = "AI"
    BUSINESS = "Business"
    BLOGGING = "Blogging"
    PHOTOGRAPHY = "Photography"
    ART = "Art"
    VIDEO = "Video"
    CRYPTO = "Crypto"


class ScanType(str, Enum):
    """Type of scan being performed."""
    EMAIL = "email"
    USERNAME = "username"


# ── Theme Colors (Rich markup) ──────────────────────────────────────────────

class Theme:
    """Matrix-inspired green-on-black terminal theme tokens."""
    PRIMARY = "bright_green"
    SECONDARY = "green"
    ACCENT = "bright_cyan"
    FOUND = "bold bright_green"
    NOT_FOUND = "dim white"
    ERROR = "bold red"
    UNKNOWN = "yellow"
    HEADER = "bold bright_green on black"
    BANNER = "bright_green"
    MUTED = "dim green"
    URL = "underline bright_cyan"
    PROGRESS = "bright_green"
    TABLE_BORDER = "green"
    TABLE_HEADER = "bold bright_green"
    PROMPT = "bright_green"
    SUCCESS = "bold bright_green"
    WARNING = "bold yellow"
    INFO = "bold bright_cyan"


# ── Defaults ─────────────────────────────────────────────────────────────────

DEFAULT_TIMEOUT = 5
DEFAULT_CONCURRENCY = 100
DEFAULT_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0
DEFAULT_CACHE_TTL = 3600
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

STATUS_STYLE_MAP: dict[str, str] = {
    Status.FOUND: Theme.FOUND,
    Status.NOT_FOUND: Theme.NOT_FOUND,
    Status.REGISTERED: Theme.FOUND,
    Status.NOT_REGISTERED: Theme.NOT_FOUND,
    Status.UNKNOWN: Theme.UNKNOWN,
    Status.ERROR: Theme.ERROR,
}

BANNER = r"""
[bright_green]
 ██╗   ██╗ ██████╗ ██╗██████╗ ██╗     ███████╗███╗   ██╗███████╗
 ██║   ██║██╔═══██╗██║██╔══██╗██║     ██╔════╝████╗  ██║██╔════╝
 ██║   ██║██║   ██║██║██║  ██║██║     █████╗  ██╔██╗ ██║███████╗
 ╚██╗ ██╔╝██║   ██║██║██║  ██║██║     ██╔══╝  ██║╚██╗██║╚════██║
  ╚████╔╝ ╚██████╔╝██║██████╔╝███████╗███████╗██║ ╚████║███████║
   ╚═══╝   ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
[/bright_green]
[dim green]          ── Peer into the digital void ──           v{version}[/dim green]
"""
