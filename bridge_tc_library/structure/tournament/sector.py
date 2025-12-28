from typing import Dict, Type, TYPE_CHECKING

from .table import Table
from bridge_tc_library.structure.core import BoardGroup, Status

if TYPE_CHECKING:
    from bridge_tc_library.structure.movements import BaseMovement


class Sector:
    def __init__(self, name, min_boards=0, max_boards=0):
        self.movement = None
        self.movement_cls = None
        self.name = name
        self.tables = []
        self.board_groups: Dict[int, 'BoardGroup'] = {}
        self.max_boards = 0
        self.min_boards = 0
        self.status: Status = Status.INACTIVE

    def set_movement(self, movement_cls: Type['BaseMovement']):
        self.movement_cls = movement_cls

    def add_tables(self, table: int | list[Table] | Table):
        def _clone_table(src: Table) -> Table:
            tbl = Table(src.table_id, sector=self, isplayable=src.isplayable)
            tbl.current_round = src.current_round
            tbl.current_pairs = src.current_pairs
            tbl.current_board = src.current_board
            tbl.current_board_set = src.current_board_set
            tbl.status = src.status
            tbl.og_sector = src.og_sector
            return tbl

        detach = getattr(self, "_add_detach_default", True)

        if isinstance(table, int):
            for i in range(table):
                tbl = Table(i+1, sector=self)
                self.tables.append(tbl)
        elif isinstance(table, Table):
            if detach:
                table.change_sector(self)
            else:
                self.tables.append(_clone_table(table))
        else:
            items = list(table)
            if detach:
                for t in items:
                    t.change_sector(self)
            else:
                for t in items:
                    self.tables.append(_clone_table(t))

    def remove_tables(self, table: Table | list[Table] | int):
        # Accept a single Table, an integer id, or any iterable of Tables/ids
        if not isinstance(table, (list, tuple)):
            table = [table]

        for t in table:
            target = None
            if isinstance(t, Table):
                if t in self.tables:
                    target = t
                else:
                    for cand in self.tables:
                        if cand.table_id == t.table_id:
                            target = cand
                            break
            else:
                for cand in self.tables:
                    if getattr(cand, 'table_id', None) == t:
                        target = cand
                        break

            if target is None:
                raise ValueError(f"Table {t} not found in sector {self.name}")

            target.change_sector(None)

    def advance_round(self):
        for table in self.tables:
            table.next_round()
    
    def __add__(self, other: Table | list[Table] | int) -> 'Sector':
        """Return a new Sector with `other` added without mutating self.

        `other` may be a single `Table`, a list/iterable of `Table`, or an
        integer (number of new tables to create). The operation is
        non-destructive: the original `Table` objects are cloned into the
        returned Sector so the source sector and tables remain unchanged.
        """
        new = self.copy()
        setattr(new, "_add_detach_default", False)
        try:
            new.add_tables(other)
        finally:
            if hasattr(new, "_add_detach_default"):
                delattr(new, "_add_detach_default")
        return new
    
    def __iadd__(self, other: Table | list[Table] | int) -> 'Sector':
        """In-place add: modify this Sector by adding `other`.

        `other` may be a Table, a list of Tables, or an int (number of new
        tables to create).
        """
        self.add_tables(other)
        return self

    def __isub__(self, other: Table | list[Table] | int) -> 'Sector':
        """In-place subtraction: remove `other` from this Sector."""
        self.remove_tables(other)
        return self

    def __sub__(self, other: Table | list[Table] | int) -> 'Sector':
        """Non-destructive subtraction: return a new Sector with `other`
        removed, leaving this Sector unchanged.
        """
        new = self.copy()
        new.remove_tables(other)
        return new

    def copy(self) -> 'Sector':
        """Return a shallow copy of this Sector with cloned Table objects.

        The returned Sector shares immutable configuration (movement_cls,
        board_groups mapping) but owns distinct `Table` instances so
        subsequent mutations to tables in the copy won't affect the source.
        """
        new = Sector(self.name, min_boards=self.min_boards, max_boards=self.max_boards)
        new.movement_cls = self.movement_cls
        new.movement = self.movement
        new.board_groups = self.board_groups.copy()
        new.max_boards = self.max_boards
        new.min_boards = self.min_boards
        new.status = self.status

        for t in self.tables:
            tbl = Table(t.table_id, sector=new, isplayable=t.isplayable)
            tbl.current_round = t.current_round
            tbl.current_pairs = t.current_pairs
            tbl.current_board = t.current_board
            tbl.current_board_set = t.current_board_set
            tbl.status = t.status
            tbl.og_sector = t.og_sector
            new.tables.append(tbl)

        return new