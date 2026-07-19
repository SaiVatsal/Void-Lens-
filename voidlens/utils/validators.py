"""
VoidLens validators — input validation and sanitization.

Validates emails, usernames, and filenames to prevent injection
and ensure safe operation.
"""

from __future__ import annotations

import re
from pathlib import Path


EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

USERNAME_PATTERN = re.compile(
    r"^[a-zA-Z0-9._-]{1,64}$"
)

UNSAFE_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def validate_email(email: str) -> bool:
    """Check if the email address is syntactically valid."""
    return bool(EMAIL_PATTERN.match(email.strip()))


def validate_username(username: str) -> bool:
    """Check if the username contains only safe characters."""
    return bool(USERNAME_PATTERN.match(username.strip()))


def sanitize_filename(name: str) -> str:
    """Remove unsafe characters from a filename."""
    sanitized = UNSAFE_FILENAME_CHARS.sub("_", name)
    return sanitized[:255]


def validate_file_path(path: str) -> bool:
    """Check if a file path exists and is readable."""
    return Path(path).exists() and Path(path).is_file()
