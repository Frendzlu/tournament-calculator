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

	def __init__(self, tables: list['Table'], board_groups: list['BoardGroup'], pairs: list[Pair], movement_strategies: MovementStrategy, initial_sitting: Dict['Table', Dict[Position, Pair]] = None, initial_boardgroups_placement: Dict['Table', 'BoardGroup'] = None):
		self.tables = tables
		self.board_groups = board_groups
		self.pairs = pairs
		self.movement_strategies = movement_strategies
		self.initial_sitting = initial_sitting
		self.initial_boardgroups_placement = initial_boardgroups_placement
	def get_sitting_for_round(self, round_number: int) -> Dict['Table', Dict[Position, Pair]]:
		"""
		{(table_name, position): Pair}
		"""
		self.out : Dict['Table', Dict[Position, Pair]] = {}
		self.round_number = round_number
		for i in range(round_number):
			# apply movement strategy for each round up to round_number
			#this is a placeholder for the actual logic , which will be implememnted once the initial structure is defined
			pass


	def get_boards_for_round(self, round_number: int) -> Dict['Table', 'BoardGroup']:
		"""
		{table_name: BoardGroup}
		"""
		pass

	def construct_movement(self, rounds: int) -> Dict[int, Dict['Table', Tuple[Dict[Position, Pair], 'BoardGroup']]]:
		"""
		Docstring for construct_movement
		
		:param self: Description
		:param rounds: Description
		:type rounds: int
		:return: Description
		:rtype: Dict[int, Dict[Table, Dict[Position, Pair]]]
		"""
		pass