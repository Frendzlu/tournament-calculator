from bridge_tc_library.structure.movements.strategy import MovementStrategy
from bridge_tc_library.structure.core import Position, Pair, BoardGroup, Player
from bridge_tc_library.structure.movements.movement import BaseMovement
from typing import Dict
from bridge_tc_library.structure.tournament import Table, Sector

if __name__ == '__main__':
    # Example usage of BaseMovement with MovementStrategy
    sector = Sector('A')
    tables = [Table(i + 1, sector) for i in range(6)]
    tables[3].isplayable = False  # Make one table a storage table
    tables[5].isplayable = False  # Make another table a storage table

    pairs = [Pair(i + 1, (Player(f"Player {2*i+1}"), Player(f"Player {2*i+2}"))) for i in range(8)]
    board_groups = [BoardGroup(i+1, list(range(i*3+1, i*3+4))) for i in range(7)]
    ftables = [t for t in tables if t.isplayable]

    howell_7rounds_4tables = MovementStrategy([(
        [((ftables[0], Position.EW), (ftables[3], Position.NS)),
         ((ftables[3], Position.NS), (ftables[1], Position.NS)),
         ((ftables[1], Position.NS), (ftables[1], Position.EW)),
         ((ftables[1], Position.EW), (ftables[2], Position.NS)),
         ((ftables[2], Position.NS), (ftables[3], Position.EW)),
         ((ftables[2], Position.EW), (ftables[0], Position.EW)),
         ((ftables[3], Position.EW), (ftables[2], Position.EW)),        
        ],
        [(tables[0], tables[5]),
         (tables[5], tables[4]),
         (tables[4], tables[3]),
         (tables[3], tables[2]),
         (tables[2], tables[1]),
         (tables[1], tables[0])],
        [1, 2, 3, 4, 5, 6, 7]
    )])

    movement = BaseMovement(tables=tables, board_groups=board_groups, pairs=pairs, movement_strategies=howell_7rounds_4tables)
    sector.set_movement(movement)

    a = movement.movement_strategies.get_strategy_for_round(1)
    movement.autogenerate_initial_sitting()
    movement.autogenerate_initial_boardgroup_placement()
    movement.construct_movement(3)
    print(sector.get_sector_as_string_for_round(1))
    print(sector.get_sector_as_string_for_round(2))
    print(sector.get_sector_as_string_for_round(3))
    sector.exclude_storage_tables_from_numbering()
    print(sector.get_sector_as_string_for_round(1))
    print(sector.get_sector_as_string_for_round(2))
    print(sector.get_sector_as_string_for_round(3))

    print("range(5)")
    for i in range(5):
        print(i)
    print("range(1,5)")
    for i in range(1, 5):
        print(i)
    print("range(3,5)")
    for i in range(3, 5):
        print(i)
    print("range(4,5)")
    for i in range(4, 5):
        print(i)