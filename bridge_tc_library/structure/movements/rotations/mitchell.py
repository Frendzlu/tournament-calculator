<<<<<<< HEAD
from typing import List, Dict, Tuple, Any

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation
from bridge_tc_library.structure.core import Position
from bridge_tc_library.structure.tournament import Table
=======
from collections import deque
from typing import List, Dict, Tuple, Any, TYPE_CHECKING

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation, RotationParams

if TYPE_CHECKING:
	from bridge_tc_library.structure.tournament import Table
>>>>>>> 56e97a720447ccf7d4bdc916fcb070646c4ae7e2


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
	
	def ask_if_rotate_boards(self, num_rounds: int) -> int:
		"""
		This function, will be asking when and if boards are to be rotated NS <-> EW 
		"""
		raise NotImplementedError("Query asking when boards are to be rotated is not yet implemented.")


	def generate_strategy_for_rotation(self, num_pairs: int, num_rounds: int, num_boardgroup_sets: int, Tables: Tuple[Table], rotate_boards_after_round: int = None) -> MovementStrategy:
		"""
		for rounds before ns <-> ew switch: table n NS -> table n NS, table n EW -> table n+1 EW
		for switch round: table n NS -> table n EW, table n EW -> table n+1 NS
		for rounds after switch: table n NS -> table n+1 NS, table n EW -> table n EW
		"""
		movement_strategy: MovementStrategy = []
		player_change_list: List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]] = []
		board_change_list: List[Tuple['Table', 'Table']] = []
		turn_list: List[int] = []
		if ((rotate_boards_after_round is None) or ((rotate_boards_after_round is not None) and (rotate_boards_after_round != 0))):
			#We check if we need to create pre switch rotation_strategy
			
			if rotate_boards_after_round is not None:
				num_rounds_pre_switch: int = rotate_boards_after_round - 1
			else:
				num_rounds_pre_switch: int = num_rounds
			print("print something so vscode does not cream at me for invalid indentations")
		return movement_strategy