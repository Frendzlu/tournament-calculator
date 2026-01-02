from collections import deque
from typing import List, Dict, Tuple, Any, TYPE_CHECKING

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation, RotationParams

if TYPE_CHECKING:
	from bridge_tc_library.structure.tournament import Table


class MitchellMovement(AbstractRotation):
	"""
	Standalone Mitchell movements generator inheriting shared helpers.
	Mitchell operates always on just one boardgroup_set, and it always uses boards_amount = tables_amount * n were n = {1, 2, 3, ...}
	"""

	def __init__(self, tables: List['Table']):
		super().__init__(tables)
		num_tables = len(tables)
		if num_tables < 3 or num_tables % 2 == 0:
			raise ValueError("Mitchell rotation requires an odd number of tables")

	def generate_strategy_for_rotation(self, rounds: int) -> MovementStrategy:
		pass	

	@classmethod
	def generate_possible_rotations(cls, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int) -> List[RotationParams]:
		list_of_rotations: List[RotationParams] = []
		num_tables = num_pairs // 2
		# Mitchell requires odd number of tables >= 3
		if num_tables < 3 or num_tables % 2 == 0:
			return list_of_rotations
		boards_per_boardgroup = min_boards_per_boardgroup
		while boards_per_boardgroup * num_tables <= max_boards_amount:
			if boards_per_boardgroup * num_tables >= min_boards_amount:
				# Mitchell always uses 1 boardgroup_set, num_board_groups = num_tables
				list_of_rotations.append(RotationParams(num_tables, num_tables, boards_per_boardgroup))
			boards_per_boardgroup += 1
		return list_of_rotations


	
