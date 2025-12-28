from typing import Dict, Tuple, List, TYPE_CHECKING

from .strategy import MovementStrategy
from bridge_tc_library.structure.core import Position, Pair, BoardGroup

if TYPE_CHECKING:
	# Import only for type checking to avoid circular import at runtime
	from bridge_tc_library.structure.tournament import Table


class BaseMovement:
	tables: list['Table']
	board_groups: list['BoardGroup']
	pairs: list['Pair']
	movement_strategies: MovementStrategy
	initial_sitting: Dict['Table', Dict[Position, Pair]]
	initial_boardgroup_placement: Dict['Table', list['BoardGroup']]
	round_data: Dict[int, Dict['Table', Tuple[Dict[Position, Pair], 'BoardGroup']]]

	def __init__(self, tables: list['Table'], board_groups: list['BoardGroup'], pairs: list[Pair], movement_strategies: MovementStrategy):
		self.tables = tables
		self.board_groups = board_groups
		self.pairs = pairs
		self.movement_strategies = movement_strategies
		self.initial_sitting: Dict['Table', Dict[Position, Pair]] = None
		self.initial_boardgroup_placement: Dict['Table', list['BoardGroup']] = None
		self.round_data: Dict[int, Dict['Table', Tuple[Dict[Position, Pair], 'BoardGroup']]] = {}

	def set_initial_sitting(self, initial_sitting: Dict['Table', Dict[Position, Pair]]):
		"""
		Set the initial sitting for the movement.
		"""
		self.initial_sitting = initial_sitting
	
	def set_initial_boardgroup_placement(self, initial_boardgroup_placement: Dict['Table', list['BoardGroup']]):
		"""
		Set the initial boardgroups placement for the movement.
		"""
		self.initial_boardgroup_placement = initial_boardgroup_placement

	def autogenerate_initial_sitting(self) -> Dict['Table', Dict[Position, Pair]]:
		"""
		Creates initial_sitting if none was provided.
		Asignes pairs to tables in order.
		"""
		if self.initial_sitting is None:
			self.initial_sitting = {}
			cur = 0
			for table in self.tables:
				if table.isplayable:
					self.initial_sitting[table] = {Position.NS: self.pairs[2*cur], Position.EW: self.pairs[2*cur + 1]}
					cur += 1
			return self.initial_sitting
		if self.initial_sitting is Dict['Table', Dict[Position, Pair]]:
			return self.initial_sitting
		raise ValueError("initial_sitting must be of type Dict[Table, Dict[Position, Pair]]")
	
	def autogenerate_initial_boardgroup_placement(self) -> Dict['Table', list['BoardGroup']]:
		"""
		Creates initial_boardgroup_placement if none was provided.
		Iterates through tables and board_groups in order. Assumes they are aligned.
		Returns the initial_boardgroup_placement.
		"""
		if self.initial_boardgroup_placement is Dict['Table', list['BoardGroup']]:
			return self.initial_boardgroup_placement
		else:
			self.initial_boardgroup_placement = {}
			#it will not work if number of board groups is different than number of tables
			for table, boardgroup in zip(self.tables, self.board_groups):
				self.initial_boardgroup_placement[table] = [boardgroup]
			diff = abs(len(self.tables) - len(self.board_groups))
			if diff > 0:
				if len(self.tables) < len(self.board_groups):
					print(f"Warning: There are {diff} more board groups than tables. Will assign the rest to last storage table.")
				else:
					print(f"Warning: There are {diff} more tables than board groups. Some tables will not have any board groups assigned.")
				storage_tables = [table for table in self.tables if not table.isplayable]
				if storage_tables:
					storage_table = storage_tables[-1]
					# assign remaining board groups to the last storage table
					self.initial_boardgroup_placement[storage_table] += self.board_groups[len(self.tables):]
				else: 
					raise ValueError("No storage table available to assign remaining board groups.")
					# TODO: should create storage table automatically? for now, raise error
		return self.initial_boardgroup_placement

	def get_sitting_for_round(self, round_number: int) -> Dict['Table', Dict[Position, Pair]]:
		"""
		{(table_name, position): Pair}
		"""
		
		if round_number == 1:
			return self.initial_sitting
		else:
			if self.round_data.get(round_number):
				sitting_for_round = {}
				for table, (sitting, _) in self.round_data[round_number].items():
					# Only include tables that have both NS and EW positions filled
					if sitting and Position.NS in sitting and Position.EW in sitting:
						sitting_for_round[table] = sitting
				return sitting_for_round
			else:
				raise ValueError(f"Sitting for round {round_number} not found. Make sure to run construct_movement first.")


	def get_boards_for_round(self, round_number: int) -> Dict['Table', 'BoardGroup']:
		"""
		{table_name: BoardGroup}
		"""
		
		if round_number == 1:
			return self.initial_boardgroup_placement
		else:
			if self.round_data.get(round_number):
				boards_for_round = {}
				for table, (_, boardgroup) in self.round_data[round_number].items():
					boards_for_round[table] = boardgroup
				return boards_for_round
			else:
				raise ValueError(f"Board placement for round {round_number} not found. Make sure to run construct_movement first.")

	def construct_movement(self, rounds: int) -> Dict[int, Dict['Table', Tuple[Dict[Position, Pair], List['BoardGroup']]]]:
		"""
		Construct round_data for all rounds based on initial state and movement strategies.
		Uses simultaneous-move semantics for pairs and FIFO queue semantics for board-groups.
		"""
		self.round_data = {}

		# Round 1: copy from initial state
		self.round_data[1] = {
			table: (dict(self.initial_sitting.get(table, {})), list(self.initial_boardgroup_placement.get(table, [])))
			for table in self.tables
		}

		for rnd in range(2, rounds + 1):
			player_moves, board_moves = self.movement_strategies.get_strategy_for_round(rnd)
			prev = self.round_data[rnd - 1]

			# Snapshot previous state
			prev_sit = {t: dict(prev[t][0]) for t in self.tables}
			prev_bg = {t: list(prev[t][1]) for t in self.tables}

			# Apply pair moves: read from snapshot, write destinations
			new_sit = {t: {} for t in self.tables}
			filled = set()
			for (src_tbl, src_pos), (dst_tbl, dst_pos) in player_moves:
				pair = prev_sit[src_tbl].get(src_pos)
				if pair:
					new_sit[dst_tbl][dst_pos] = pair
					filled.add((dst_tbl, dst_pos))

			# Carry over unchanged positions
			for t in self.tables:
				for pos, pair in prev_sit[t].items():
					if (t, pos) not in filled:
						new_sit[t][pos] = pair

			# Apply board-group moves: FIFO pop from source, append to destination
			new_bg = {t: list(prev_bg[t]) for t in self.tables}
			for src_tbl, dst_tbl in board_moves:
				if prev_bg[src_tbl]:
					bg = prev_bg[src_tbl].pop(0)
					new_bg[src_tbl].pop(0)
					new_bg[dst_tbl].append(bg)

			self.round_data[rnd] = {t: (new_sit[t], new_bg[t]) for t in self.tables}

		return self.round_data