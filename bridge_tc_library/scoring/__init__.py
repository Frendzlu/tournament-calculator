"""Scoring utilities for tournament calculator.

This package contains a `ScoreCalculator` which consumes a validated
`Tournament` and a BWS representation to compute match/board scores. The
implementation here is a placeholder API; replace scoring logic with real
bridge scoring algorithms as needed.
"""
from .calculator import ScoreCalculator

__all__ = ["ScoreCalculator"]
