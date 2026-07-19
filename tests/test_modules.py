"""Tests for module discovery and registration."""

from voidlens.email_scan import get_all_modules as get_email_modules
from voidlens.username_scan import get_all_modules as get_username_modules
from voidlens.email_scan.base import BaseEmailModule
from voidlens.username_scan.base import BaseUsernameModule


def test_email_modules_discovered():
    modules = get_email_modules()
    assert len(modules) >= 10
    for name, mod in modules.items():
        assert isinstance(mod, BaseEmailModule)
        meta = mod.metadata()
        assert "name" in meta
        assert "url" in meta
        assert "category" in meta


def test_username_modules_discovered():
    modules = get_username_modules()
    assert len(modules) >= 10
    for name, mod in modules.items():
        assert isinstance(mod, BaseUsernameModule)
        meta = mod.metadata()
        assert "name" in meta
        assert "url" in meta
        assert "category" in meta


def test_email_module_names():
    modules = get_email_modules()
    expected = ["github", "gravatar", "spotify", "discord", "reddit",
                "steam", "gitlab", "wordpress"]
    for name in expected:
        assert name in modules, f"Missing email module: {name}"


def test_username_module_names():
    modules = get_username_modules()
    expected = ["github", "reddit", "twitter", "instagram", "steam",
                "gitlab", "medium", "hackernews", "keybase"]
    for name in expected:
        assert name in modules, f"Missing username module: {name}"
