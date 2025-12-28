from typing import Optional, TYPE_CHECKING
from bridge_movement.core.status import Status

if TYPE_CHECKING:
    from .sector import Sector
    from bridge_movement import Pair, Position, BoardGroup
    

class Table:
    def __init__(self, table_id: int, sector: 'Sector', isplayable: bool = True) -> None:
        self.table_id: int = table_id
        self.sector: 'Sector' = sector
        self.isplayable: bool = isplayable
        self.current_round: Optional[int] = None
        self.current_pairs: Optional[dict['Position', 'Pair']] = None
        self.current_board: Optional[int] = None
        self.current_board_set: Optional['BoardGroup'] = None
        self.status: Status = Status.INACTIVE

    def start(self, ns_pair: 'Pair', ew_pair: 'Pair', board_set: 'BoardGroup'):
        self.current_round = 1
        self.current_pairs = {
            Position.NS: ns_pair,
            Position.EW: ew_pair
        }
        self.current_board = board_set.boards[0]
        self.current_board_set = board_set
        self.status = Status.ACTIVE

    def next_deal(self):
        if self.current_round is None:
            raise ValueError("Table has not started any round yet.")

        if self.current_board_set.boards.index(self.current_board) + 1 > len(self.current_board_set.boards):
            next_index = self.current_board_set.boards.index(self.current_board) + 1
            self.current_board = self.current_board_set.boards[next_index]
