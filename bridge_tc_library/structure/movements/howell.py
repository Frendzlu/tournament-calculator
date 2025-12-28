from collections import deque
from typing import List, Dict, Tuple, Any
from .generator import MovementGenerator


class HowellMovement(MovementGenerator):
	"""
	Standalone Howell movements generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int):
		super().__init__()
		if num_pairs % 2 != 0:
			raise ValueError("num_pairs must be even")
		self.num_pairs = num_pairs
		self.num_tables = num_pairs // 2
		# do not set pair_rounds here; MovementGenerator will compute them

	def _wheel_base(self) -> List[str]:
		pairs = [str(i + 1) for i in range(self.num_pairs)]
		numeric_sorted = sorted(pairs, key=lambda x: int(x))
		stationary = numeric_sorted[-1]
		others = [p for p in numeric_sorted if p != stationary]
		if others:
			wheel_base = others[1:] + [others[0]] if len(others) > 1 else [others[0]]
		else:
			wheel_base = []
		return [stationary] + wheel_base

	def initial_round(self) -> Dict[Tuple[int, str], Any]:
		# build initial positions from wheel_base rotated so that '1' is at index num_tables-1
		base = self._wheel_base()
		stationary = base[0]
		wheel = base[1:]
		if wheel:
			try:
				idx1 = next(i for i, p in enumerate(wheel) if p == '1')
			except StopIteration:
				idx1 = 0
			dq = deque(wheel)
			dq.rotate((self.num_tables - 1 - idx1) % len(wheel))
			positions = [stationary] + list(dq)
		else:
			positions = [stationary]
		# compose initial round_map
		round_map = {}
		for i in range(self.num_tables):
			round_map[(i + 1, 'NS')] = positions[i]
			round_map[(i + 1, 'EW')] = positions[i + self.num_tables]
		return round_map

	def step(self, round_map: Dict[Tuple[int, str], Any]) -> Dict[Tuple[int, str], Any]:
		# Howell wheel rotates all non-stationary pairs; we'll rotate the wheel part
		stationary = None
		# reconstruct wheel from current map
		pairs_by_index = [None] * (2 * self.num_tables)
		for (t, pos), p in round_map.items():
			if pos == 'NS':
				pairs_by_index[t - 1] = p
			else:
				pairs_by_index[(t - 1) + self.num_tables] = p
		# rotate the wheel section (excluding stationary) by -1
		# find stationary at index 0
		wheel = pairs_by_index[1:self.num_tables] + pairs_by_index[self.num_tables + 1:]
		dq = deque(wheel)
		dq.rotate(-1)
		# rebuild positions: keep stationary at index 0, fill others from rotated dq
		new_positions = [pairs_by_index[0]] + list(dq[:self.num_tables - 1])
		# for EW side, take the remaining elements
		ew_positions = list(dq[self.num_tables - 1:])
		new_map = {}
		for i in range(self.num_tables):
			new_map[(i + 1, 'NS')] = new_positions[i]
			new_map[(i + 1, 'EW')] = ew_positions[i] if i < len(ew_positions) else None
		return new_map
