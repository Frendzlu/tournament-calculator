from collections import deque
from typing import List, Dict, Tuple, Any
from bridge_tc_library.structure.movements.rotation_calculator import RotationCalculator


class HowellMovement(RotationCalculator):
	"""
	Standalone Howell movements generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int):
		super().__init__()
		