"""
VoidLens email_scan package — auto-discovery registry for email modules.

Drop a new .py module in this directory and it will be automatically
registered. Each module must contain a class that subclasses BaseEmailModule.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Type

from voidlens.email_scan.base import BaseEmailModule

_registry: dict[str, BaseEmailModule] = {}


def _discover_modules() -> None:
    """Scan this package directory and register all BaseEmailModule subclasses."""
    package_dir = Path(__file__).parent
    for importer, modname, ispkg in pkgutil.iter_modules([str(package_dir)]):
        if modname == "base":
            continue
        try:
            module = importlib.import_module(f"voidlens.email_scan.{modname}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseEmailModule)
                    and attr is not BaseEmailModule
                ):
                    instance = attr()
                    meta = instance.metadata()
                    _registry[meta["name"].lower()] = instance
        except Exception:
            continue


def get_all_modules() -> dict[str, BaseEmailModule]:
    """Return all registered email modules."""
    if not _registry:
        _discover_modules()
    return _registry


def get_module(name: str) -> BaseEmailModule | None:
    """Get a specific email module by name."""
    modules = get_all_modules()
    return modules.get(name.lower())


def get_modules_by_category(category: str) -> list[BaseEmailModule]:
    """Filter modules by category."""
    modules = get_all_modules()
    return [m for m in modules.values() if m.category().lower() == category.lower()]
