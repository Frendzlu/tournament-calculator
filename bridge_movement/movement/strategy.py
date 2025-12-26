from typing import List, Tuple
from bridge_movement.core import Position
from bridge_movement.tournament.table import Table

class MovStrat:
    """
    Movement strategy container.

    Internally stores a list of 2-tuples: (change_list, rounds_list)
    - change_list: list of tuples ((Table, Position), (Table, Position)) indicating pair moves (from, to)
    - rounds_list: list[int] specifying rounds when this change_list applies
    """

    def __init__(self, strategies: List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[int]]]):
        # minimal structural validation
        if not isinstance(strategies, list):
            raise TypeError("MovStrat expects a list of (change_list, rounds_list) tuples")
        self.strategies = []
        for item in strategies:
            if not (isinstance(item, tuple) or isinstance(item, list)) or len(item) != 2:
                raise TypeError("each strategy must be a 2-tuple: (change_list, rounds_list)")
            change_list, rounds = item
            if not isinstance(change_list, list):
                raise TypeError("change_list must be a list")
            if not isinstance(rounds, list):
                raise TypeError("rounds must be a list of ints")
            self.strategies.append((change_list, rounds))

    def as_list(self) -> List[Tuple[List[Tuple[Tuple['Table', Position], Tuple['Table', Position]]], List[int]]]:
        return self.strategies

    def __repr__(self) -> str:
        return f"MovStrat({len(self.strategies)} strategies)"