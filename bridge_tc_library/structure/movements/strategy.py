from typing import List, Tuple, TYPE_CHECKING
from bridge_tc_library.structure.core import Position

if TYPE_CHECKING:
    from bridge_tc_library.structure.tournament.table import Table

class MovementStrategy:
    """
    Movement strategy container.

    Internally stores a list of 2-tuples: (player_change_list, board_change_list, rounds_list)
    - player_change_list: list of tuples ((Table, Position), (Table, Position)) indicating pair moves (from, to)
    - board_change_list: list of tuples (Table, Table) indicating board moves (from, to)
    - rounds_list: list[int] specifying rounds when this change_list applies
    """
    strategies: List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[Tuple['Table', 'Table']], List[int]]]

    def __init__(self, strategies: List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[Tuple['Table', 'Table']], List[int]]]):
        # minimal structural validation
        if not isinstance(strategies, list):
            raise TypeError("MovStrat expects a list of (change_list, rounds_list) tuples")
        self.strategies = []
        for item in strategies:
            if not (isinstance(item, tuple) or isinstance(item, list)) or len(item) != 3:
                raise TypeError("each strategy must be a 3-tuple: (player_change_list, board_change_list, rounds_list)")
            player_change_list, board_change_list, rounds = item
            if not isinstance(player_change_list, list):
                raise TypeError("player_change_list must be a list")
            if not isinstance(board_change_list, list):
                raise TypeError("board_change_list must be a list")
            if not isinstance(rounds, list):
                raise TypeError("rounds must be a list of ints")
            self.strategies.append((player_change_list, board_change_list, rounds))

    def as_list(self) -> List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[Tuple['Table', 'Table']], List[int]]]:
        return self.strategies
    
    def get_strategy_for_round(self, round_number: int) -> Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[Tuple['Table', 'Table']]]:
        """
        Returns the player and board change lists for a specific round. Round numbers start at 1.
        Raises ValueError if no strategy is defined for the given round.
        """
        for player_change_list, board_change_list, rounds in self.strategies:
            if round_number in rounds:
                return player_change_list, board_change_list
        raise ValueError(f"No strategy defined for round {round_number}")

    def __repr__(self) -> str:
        return f"MovStrat({len(self.strategies)} strategies)"