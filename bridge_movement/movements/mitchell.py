from collections import deque
from typing import List
from .strategy import MovementStrategy
from .generator import MovementGenerator

class MitchellMovement(MovementGenerator):
	"""
	Standalone Mitchell movements generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int):
		if num_pairs % 2 != 0:
			raise ValueError("num_pairs must be even")
		self.num_pairs = num_pairs
		self.num_tables = num_pairs // 2
		self.pair_rounds = self._build_rounds()

	def _build_rounds(self) -> List[dict]:
		pairs = [str(i + 1) for i in range(self.num_pairs)]
		# initial NS first half, EW second half (numeric order)
		ns_initial = pairs[:self.num_tables]
		ew_initial = pairs[self.num_tables: self.num_tables*2]

		rounds = []
		total_rounds = 2 * self.num_tables - 1
		dq = deque(ew_initial)
		for _ in range(total_rounds):
			round_map = {}
			for i in range(self.num_tables):
				round_map[(i + 1, 'NS')] = ns_initial[i]
				round_map[(i + 1, 'EW')] = dq[i]
			rounds.append(round_map)
			dq.rotate(-1)
		return rounds
