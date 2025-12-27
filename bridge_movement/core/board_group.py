from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class BoardGroup:
	"""
	A group of board numbers played together in one round at one table.
	"""
	BoardGroupId: int
	boards: Tuple[int, ...]
