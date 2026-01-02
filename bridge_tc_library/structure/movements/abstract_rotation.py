from typing import List, Optional, Any, Tuple, Dict, NamedTuple, TYPE_CHECKING
from abc import ABC, abstractmethod
from .strategy import MovementStrategy
from bridge_tc_library.structure.core import Position

if TYPE_CHECKING:
	from bridge_tc_library.structure.tournament import Table


class RotationParams(NamedTuple):
	"""Parameters describing a possible rotation configuration."""
	num_tables: int
	num_board_groups: int
	boards_per_board_group: int


class AbstractRotation(ABC):
	num_tables: int
	"""
	Abstract base class for rotation calculators.
	"""

	def __init__(self, tables: List['Table']):
		self.tables = tables
		self._pair_rounds_cache: Optional[List[Dict[Tuple[int, str], Any]]] = None
		
	@classmethod
	@abstractmethod
	def generate_possible_rotations(cls, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int) -> List[RotationParams]:
		"""
		Generates possible rotation drafts.
		This will generate a list of possible rotations in a draft format.
		List of RotationParams: (num_tables, num_board_groups, boards_per_board_group)
		"""

	@abstractmethod
	def generate_strategy_for_rotation(self, rounds: int) -> MovementStrategy:
		"""
		Generates movement strategy for the given number of rounds.
		"""

	def check_if_bye_needed(self, num_pairs: int) -> bool:
		"""
		Indicates if bye is needed in the rotation.
		If so, one pair will be added to the total number of pairs, so it is even.
		"""
		if num_pairs % 2 == 1:
			self.num_pairs += 1
			return True
		else:
			return False

	
