"""
VoidLens pattern generator — username variation engine.

Generates username permutations using template wildcards:
    {first}, {last}, {year}, {number}, {random}
"""

from __future__ import annotations

import random
import string
from datetime import datetime


COMMON_SUFFIXES = [
    "", "1", "2", "3", "01", "02", "99", "00", "123", "007",
    "_", ".", "-", "_1", "_2", ".dev", "_dev", "x", "hd",
    "official", "real", "the", "pro", "og",
]

COMMON_PREFIXES = [
    "", "the", "real", "mr", "its", "im", "x", "official",
]


def generate_variations(base: str, count: int = 20) -> list[str]:
    """
    Generate username variations from a base string.

    Args:
        base: The base username to generate variations from.
        count: Maximum number of variations to generate.

    Returns:
        List of unique username variations.
    """
    variations: set[str] = {base}

    # Suffix variations
    for suffix in COMMON_SUFFIXES:
        variations.add(f"{base}{suffix}")

    # Prefix variations
    for prefix in COMMON_PREFIXES:
        if prefix:
            variations.add(f"{prefix}{base}")
            variations.add(f"{prefix}_{base}")
            variations.add(f"{prefix}.{base}")

    # Year variations
    current_year = datetime.now().year
    for year in range(current_year - 5, current_year + 1):
        variations.add(f"{base}{year}")
        variations.add(f"{base}{str(year)[-2:]}")

    # Number variations
    for i in range(10):
        variations.add(f"{base}{i}")

    # Random variations
    for _ in range(3):
        rand_suffix = "".join(random.choices(string.digits, k=3))
        variations.add(f"{base}{rand_suffix}")

    return sorted(list(variations))[:count]


def expand_template(template: str, **kwargs: str) -> str:
    """
    Expand a username template with wildcard substitution.

    Supported wildcards:
        {first}  — first name
        {last}   — last name
        {year}   — current year
        {number} — random 2-digit number
        {random} — random 4-char alphanumeric string

    Args:
        template: Template string with {wildcards}.
        **kwargs: Override values for wildcards.

    Returns:
        Expanded username string.
    """
    defaults = {
        "year": str(datetime.now().year),
        "number": str(random.randint(10, 99)),
        "random": "".join(random.choices(string.ascii_lowercase + string.digits, k=4)),
    }
    defaults.update(kwargs)
    try:
        return template.format(**defaults)
    except KeyError:
        return template
