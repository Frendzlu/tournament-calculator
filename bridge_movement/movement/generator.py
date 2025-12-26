from typing import List, Optional, Any, Tuple
from .base_movement import MovStrat
from bridge_movement.core import Position


class MovementGenerator:
	"""
	Common helper class for movement generators.
	Subclasses must provide:
	- self.pair_rounds: List[dict] keyed by (table_index, 'NS'/'EW') -> pair id (or Pair)
	- self.num_tables: int
	"""
	def get_round_sitting(self, round_number: int, tables: Optional[List[Any]] = None):
		idx = round_number - 1
		if idx < 0 or idx >= len(self.pair_rounds):
			raise StopIteration("Round out of range")
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

	def get_movement_strategy(self, tables: Optional[List[Any]] = None) -> MovStrat:
		strategies = []
		for r_index in range(len(self.pair_rounds)):
			prev = self.pair_rounds[r_index - 1]
			curr = self.pair_rounds[r_index]
			changes: List[Tuple[Tuple[Any, Position], Tuple[Any, Position]]] = []
			for (table_pos), p in curr.items():
				prev_p = prev.get(table_pos)
				if prev_p != p:
					if p is None:
						continue
					from_loc = None
					for (t2, pos2), pp in prev.items():
						if pp == p:
							from_loc = (t2, pos2)
							break
					to_loc = table_pos
					if from_loc:
						from_table = tables[from_loc[0] - 1] if tables else from_loc[0]
						to_table = tables[to_loc[0] - 1] if tables else to_loc[0]
						from_pos = Position(from_loc[1]) if isinstance(from_loc[1], str) else from_loc[1]
						to_pos = Position(to_loc[1]) if isinstance(to_loc[1], str) else to_loc[1]
						changes.append(((from_table, from_pos), (to_table, to_pos)))
			strategies.append((changes, [r_index + 1]))
		return MovStrat(strategies)

