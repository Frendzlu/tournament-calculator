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
        # Store the movements class for later instantiation by code that knows the
        # appropriate constructor signature.
        self.movement_cls = movement_cls

    def add_tables(self, table: int | list[Table] | Table):
        if isinstance(table, int):
            for i in range(table):
                tbl = Table(i+1, sector=self)
                self.tables.append(tbl)
        elif isinstance(table, Table):
            table.sector.remove_tables(table)
            table.sector = self
            self.tables.append(table)
        else:
            for t in table:
                t.sector.remove_tables(t)
                t.sector = self
            self.tables.extend(table)

    def remove_tables(self, table: Table | list[Table]):
        if isinstance(table, Table):
            table = [table]
        for t in table:
            t.sector = None
            self.tables.remove(t)

    def advance_round(self):
        for table in self.tables:
            table.next_round()

    def __add__(self, other: 'Sector') -> 'Sector':
        # adding sectors is not supported... yet. How would this even work?
        pass
    
    def __add__(self, other: Table) -> 'Sector':
        new_sector = Sector(name=f"{self.name}+{other}",
                            min_boards=self.min_boards + other,
                            max_boards=self.max_boards + other)
        new_sector.tables = self.tables.copy()
        for table in new_sector.tables:
            table.sector = new_sector
        new_sector.board_groups = self.board_groups.copy()
        return new_sector
