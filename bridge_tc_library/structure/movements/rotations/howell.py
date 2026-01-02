from collections import deque
from typing import List, Dict, Tuple, Any, TYPE_CHECKING

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation, RotationParams

if TYPE_CHECKING:
	from bridge_tc_library.structure.tournament import Table


class HowellMovement(AbstractRotation):
	"""
	Standalone Howell movements generator inheriting shared helpers.
	How does howell work:
	basic: all vs all, num_round = num_pairs - 1
	reduced: for bigger, (num_pairs*3/4 -1) <= num_rounds <= (num_pairs - 1)
	"""
	def __init__(self, tables: List['Table']):
		super().__init__(tables)
		self.num_pairs = len(tables) * 2
		self.bye = self.check_if_bye_needed(self.num_pairs)

	@classmethod
	def generate_possible_rotations(cls, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int) -> List[RotationParams]:
		return []

	def generate_strategy_for_rotation(self, rounds: int) -> MovementStrategy:
		pass

