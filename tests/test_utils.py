"""Tests for validators and pattern generator."""

from voidlens.utils.validators import validate_email, validate_username, sanitize_filename
from voidlens.utils.patterns import generate_variations, expand_template


def test_valid_email():
    assert validate_email("test@gmail.com") is True
    assert validate_email("user.name+tag@domain.co") is True


def test_invalid_email():
    assert validate_email("notanemail") is False
    assert validate_email("@missing.com") is False
    assert validate_email("") is False


def test_valid_username():
    assert validate_username("johndoe") is True
    assert validate_username("john_doe-123") is True
    assert validate_username("j") is True


def test_invalid_username():
    assert validate_username("") is False
    assert validate_username("user name") is False
    assert validate_username("user@name") is False


def test_sanitize_filename():
    assert sanitize_filename("report.json") == "report.json"
    assert sanitize_filename('file<>:"/\\|?*.txt') == "file_________.txt"


def test_generate_variations():
    variations = generate_variations("john", count=10)
    assert "john" in variations
    assert len(variations) <= 10
    assert all(isinstance(v, str) for v in variations)


def test_expand_template():
    result = expand_template("{first}_{last}", first="john", last="doe")
    assert result == "john_doe"


def test_expand_template_with_defaults():
    result = expand_template("user_{number}")
    assert result.startswith("user_")
    assert len(result) > 5
