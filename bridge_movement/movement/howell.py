from collections import deque
from typing import List
from .generator import MovementGenerator


class HowellMovement(MovementGenerator):
	"""
	Standalone Howell movement generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int):
		if num_pairs % 2 != 0:
			raise ValueError("num_pairs must be even")
		self.num_pairs = num_pairs
		self.num_tables = num_pairs // 2
		self.pair_rounds = self._build_rounds()

	def _build_rounds(self) -> List[dict]:
		# create pair ids as strings to match Pair.id style used elsewhere
		pairs = [str(i + 1) for i in range(self.num_pairs)]
		# Determine stationary (highest-numbered pair) and others numerically
		numeric_sorted = sorted(pairs, key=lambda x: int(x))
		stationary = numeric_sorted[-1]
		others = [p for p in numeric_sorted if p != stationary]

		# build wheel [2,3,...,S,1] behaviour
		if others:
			wheel_base = others[1:] + [others[0]] if len(others) > 1 else [others[0]]
		else:
			wheel_base = []

		dq = deque(wheel_base)
		# rotate to put '1' at index num_tables-1
		if wheel_base:
			try:
				idx1 = next(i for i, p in enumerate(wheel_base) if p == '1')
			except StopIteration:
				idx1 = 0
			dq.rotate((self.num_tables - 1 - idx1) % len(wheel_base))

		rounds = []
		total_rounds = 2 * self.num_tables - 1
		for _ in range(total_rounds):
			positions = [stationary] + list(dq)
			round_map = {}
			for i in range(self.num_tables):
				round_map[(i + 1, 'NS')] = positions[i]
				round_map[(i + 1, 'EW')] = positions[i + self.num_tables]
			rounds.append(round_map)
			dq.rotate(-1)
		return rounds

