from typing import Dict, Type, TYPE_CHECKING

from .table import Table
from bridge_movement.core import BoardGroup

if TYPE_CHECKING:
    from bridge_movement.movement import BaseMovement


class Sector:
    def __init__(self, name, min_boards=0, max_boards=0):
        self.movement = None
        self.movement_cls = None
        self.name = name
        self.tables = []
        self.board_groups: Dict[int, 'BoardGroup'] = {}
        self.max_boards = 0
        self.min_boards = 0

    def set_movement(self, movement_cls: Type['BaseMovement']):
        # Store the movement class for later instantiation by code that knows the
        # appropriate constructor signature.
        self.movement_cls = movement_cls

    def add_tables(self, table_num):
        for i in range(table_num):
            table = Table(table_id=i + 1, sector=self)
            self.tables.append(table)

    def advance_round(self):
        for table in self.tables:
            print(table)

