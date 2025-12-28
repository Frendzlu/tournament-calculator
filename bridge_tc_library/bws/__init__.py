"""BWS (Board Wise Scoring) helpers.

This subpackage provides a minimal interface for creating and maintaining a
valid BWS representation from a validated `Tournament`. Implementations below
are stubs that demonstrate the intended API surface; replace with real BWS
format handling or a live server integration as required.
"""
from .client import BWSLiveClient

__all__ = ["BWSLiveClient"]
