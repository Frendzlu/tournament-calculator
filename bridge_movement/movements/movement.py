from typing import Dict, Tuple, List, TYPE_CHECKING

from .strategy import MovementStrategy
from bridge_movement.core import Position, Pair, BoardGroup

if TYPE_CHECKING:
    # Import only for type checking to avoid circular import at runtime
    from bridge_movement.tournament import Table


class BaseMovement:
    tables: list['Table']
    boards: list['BoardGroup']
    pairs: list['Pair']

    def __init__(self, tables: list['Table'], boards: list[BoardGroup], pairs: list[Pair], movement_strategies: MovementStrategy):
        self.tables = tables
        self.boards = boards
        self.pairs = pairs
        self.movement_strategies = movement_strategies

    def get_sitting_for_round(self, round_number: int) -> Dict['Table', Dict[Position, Pair]]:
        """
        {(table_name, position): Pair}
        """
        pass

    def get_boards_for_round(self, current_boards: dict) -> dict:
        """
        {table_name: BoardGroup}
        """
        pass

