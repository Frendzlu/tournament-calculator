from typing import Optional, TYPE_CHECKING
from bridge_tc_library.structure.core.status import Status

if TYPE_CHECKING:
    from .sector import Sector
    from bridge_tc_library.structure.core import Pair, Position, BoardGroup
    

class Table:
    def __init__(self, table_id: int, sector: Optional['Sector'] = None, isplayable: bool = True) -> None:
        self._table_id: int = table_id
        self.display_id: int = table_id
        self.sector: Optional['Sector'] = sector
        self.og_sector: Optional['Sector'] = sector
        self.isplayable: bool = isplayable
        self.current_round: Optional[int] = None
        self.current_pairs: Optional[dict['Position', 'Pair']] = None
        self.current_board: Optional[int] = None
        self.current_board_set: Optional['BoardGroup'] = None
        self.status: Status = Status.INACTIVE

    def start(self, ns_pair: 'Pair', ew_pair: 'Pair', board_set: 'BoardGroup'):
        if not self.isplayable:
            raise ValueError("Cannot start a non-playable table.")
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

    def __str__(self):
        if self.isplayable:
            return f"{self.og_sector.name if self.og_sector else '_'}{self.display_id}"
        else:
            return f"_{self.og_sector.name if self.og_sector else '_'}{self.display_id}"

    def __repr__(self):
        return f"<Table _id={self._table_id} display_id={self.display_id} og_sector={self.og_sector.name if self.og_sector else '_'} sector={self.sector.name if self.sector else '_'} status={self.status.name} playable={self.isplayable}>"
    
    def change_sector(self, new_sector: Optional['Sector']):
        if self.og_sector is None:
            self.og_sector = new_sector

        old = self.sector
        if old is new_sector:
            return

        if old is not None and self in old.tables:
            old.tables.remove(self)

        self.sector = new_sector
        if new_sector is not None and self not in new_sector.tables:
            new_sector.tables.append(self)