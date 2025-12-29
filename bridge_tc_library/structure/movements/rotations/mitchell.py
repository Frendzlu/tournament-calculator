from collections import deque
from typing import List, Dict, Tuple, Any
from bridge_tc_library.structure.movements.rotation_calculator import RotationCalculator


class MitchellMovement(RotationCalculator):
	"""
	Standalone Mitchell movements generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int):
		super().__init__()
		self.num_pairs = num_pairs
		self.min_boards_amount = min_boards_amount
		self.max_boards_amount = max_boards_amount
		self.pauza = self.check_if_pauza_needed(self.num_pairs)
	
