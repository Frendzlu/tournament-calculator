from collections import deque
from typing import List, Dict, Tuple, Any, Optional, TYPE_CHECKING

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation, RotationParams

if TYPE_CHECKING:
	from bridge_tc_library.structure.tournament import Table
	from bridge_tc_library.structure.core import Position

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

	def generate_strategy_for_rotation(self, rounds: int, switch_round_num: Optional[int] = None) -> MovementStrategy:
		"""
		for rounds before ns <-> ew switch: table n NS -> table n NS, table n EW -> table n+1 EW
		for switch round: table n NS -> table n EW, table n EW -> table n+1 NS
		for rounds after switch: table n NS -> table n+1 NS, table n EW -> table n EW
		"""
		strategies: List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[Tuple['Table', 'Table']], List[int]]] = []

		#board_change_list, it will always be the same, so i can make it here and duplicate it for differrent player change lists
		board_change_list: list[Tuple[Table, Table]] = []
		for tn in range(len(self.tables)):
			board_change_list.append(Tuple[self.tables[tn], self.tables[tn - 1]])

		#player change list
		if ((switch_round_num is not None) and (switch_round_num > rounds)):
			raise ValueError(f"switch round is not existing round, it must be max {rounds}")
		if switch_round_num is None:
			switch_round_num = rounds #setting switch round at the last round which will not be recorded, but will help with simplifiing code
		if switch_round_num < 0:
			switch_round_num = 0


		if switch_round_num > 0:
			#check if we need to generate pre_switch strategy, when switch <= 0 we start rotation after the switch
			player_pre_switch_change_list: list[Tuple[Tuple[Table, Position], Tuple[Table, Position]]] = []
			rounds_pre_switch_list: list[int] = []
			for tn in range(len(self.tables)):
				player_pre_switch_change_list.append(Tuple[Tuple[self.tables[tn - 1], Position.EW], Tuple[self.tables[tn], Position.EW]])
				player_pre_switch_change_list.append(Tuple[Tuple[self.tables[tn], Position.NS], Tuple[self.tables[tn], Position.NS]])
			for r in range(1, switch_round_num - 1):
				rounds_pre_switch_list.append(r) 
			strategies.append(Tuple[player_pre_switch_change_list, board_change_list, rounds_pre_switch_list])
			if switch_round_num < rounds:
				#when we have any rounds pre_switch, check if we have a switch
				player_switch_change_list: list[Tuple[Tuple[Table, Position], Tuple[Table, Position]]] = []
				rounds_switch_list: list[int] = []
				for tn in range(len(self.tables)):
					player_switch_change_list.append(Tuple[Tuple[self.tables[tn - 1], Position.EW], Tuple[self.tables[tn], Position.NS]])
					player_switch_change_list.append(Tuple[Tuple[self.tables[tn], Position.NS], Tuple[self.tables[tn], Position.EW]])
				rounds_switch_list.append(switch_round_num)
				strategies.append(Tuple[player_switch_change_list, board_change_list, rounds_switch_list])

		if switch_round_num < rounds -1:
			#checking if any post_switch rounds exist
			player_post_switch_change_list: list[Tuple[Tuple[Table, Position], Tuple[Table, Position]]] = []
			rounds_post_switch: list[int] = []
			for tn in range(len(self.tables)):
				player_pre_switch_change_list.append(Tuple[Tuple[self.tables[tn - 1], Position.NS], Tuple[self.tables[tn], Position.NS]])
				player_pre_switch_change_list.append(Tuple[Tuple[self.tables[tn], Position.EW], Tuple[self.tables[tn], Position.EW]])
			for i in range((switch_round_num + 1), (rounds - 1)):
				rounds_post_switch.append(i)
			strategies.append(Tuple[player_post_switch_change_list, board_change_list, rounds_post_switch])

		return MovementStrategy(strategies)

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


