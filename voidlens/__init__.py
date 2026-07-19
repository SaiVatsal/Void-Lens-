"""
VoidLens — Peer into the digital void.

A professional OSINT & Digital Footprint Intelligence Suite.
"""

__version__ = "1.0.0"
__author__ = "VoidLens Contributors"

from voidlens.core.runner import scan_email, scan_username

__all__ = ["scan_email", "scan_username", "__version__"]
