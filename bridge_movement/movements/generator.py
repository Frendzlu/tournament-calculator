from typing import List, Optional, Any, Tuple, Dict
from abc import ABC, abstractmethod
from .strategy import MovementStrategy
from bridge_movement.core import Position


class MovementGenerator(ABC):
	num_tables: int

	def __init__(self):
		self._pair_rounds_cache: Optional[List[Dict[Tuple[int, str], Any]]] = None

	@abstractmethod
	def initial_round(self) -> Dict[Tuple[int, str], Any]:
		raise NotImplementedError

	@abstractmethod
	def step(self, round_map: Dict[Tuple[int, str], Any]) -> Dict[Tuple[int, str], Any]:
		raise NotImplementedError

	@property
	def pair_rounds(self) -> List[Dict[Tuple[int, str], Any]]:
		if getattr(self, '_pair_rounds_cache', None) is None:
			rounds: List[Dict[Tuple[int, str], Any]] = []
			seen: List[Dict[Tuple[int, str], Any]] = []
			curr = self.initial_round()
			while True:
				# stop when a configuration repeats
				if any(curr == r for r in seen):
					break
				rounds.append(curr)
				seen.append(curr)
				curr = self.step(curr)
			setattr(self, '_pair_rounds_cache', rounds)
		return getattr(self, '_pair_rounds_cache')

	def get_round_sitting(self, round_number: int, tables: Optional[List[Any]] = None):
		if round_number < 1:
			raise StopIteration("Round numbers start at 1")
		if not self.pair_rounds:
			raise StopIteration("No rounds available")
		idx = (round_number - 1) % len(self.pair_rounds)
		round_map = self.pair_rounds[idx]
		if not tables:
			return round_map
		if len(tables) != self.num_tables:
			raise ValueError("tables length must equal number of tables for this movement")
		out = {}
		for i, tbl in enumerate(tables):
			ns = round_map[(i + 1, 'NS')]
			ew = round_map[(i + 1, 'EW')]
			out[tbl] = {
				Position.NS: ns,
				Position.EW: ew
			}
		return out

	def get_movement_strategy(self, tables: Optional[List[Any]] = None) -> MovementStrategy:
		n = len(self.pair_rounds)
		if n == 0:
			return MovementStrategy([])
		# choose reference transition curr -> next (round 1 -> round 2)
		curr = self.pair_rounds[0]
		next_round = self.pair_rounds[(0 + 1) % n]
		changes: List[Tuple[Tuple[Any, Position], Tuple[Any, Position]]] = []
		for (table_pos), p in next_round.items():
			# find where this pair was in curr
			if p is None:
				continue
			from_loc = None
			for (t2, pos2), pp in curr.items():
				if pp == p:
					from_loc = (t2, pos2)
					break
			if from_loc:
				# map table indices to Table objects if provided
				from_table = tables[from_loc[0] - 1] if tables else from_loc[0]
				to_table = tables[table_pos[0] - 1] if tables else table_pos[0]
				from_pos = Position(from_loc[1]) if isinstance(from_loc[1], str) else from_loc[1]
				to_pos = Position(table_pos[1]) if isinstance(table_pos[1], str) else table_pos[1]
				changes.append(((from_table, from_pos), (to_table, to_pos)))
		# Apply same change_list to all rounds
		rounds_list = list(range(1, n + 1))
		return MovementStrategy([(changes, rounds_list)])
