from bridge_tc_library.structure.movements.strategy import MovementStrategy
from bridge_tc_library.structure.core import Position, Pair, BoardGroup, Player
from bridge_tc_library.structure.movements.movement import BaseMovement
from bridge_tc_library.structure.tournament import Table, Sector

sector = Sector('A')
tables = [Table(i + 1, sector) for i in range(6)]
tables[3].isplayable = False
tables[5].isplayable = False
pairs = [Pair(i + 1, (Player(f"Player {2*i+1}"), Player(f"Player {2*i+2}"))) for i in range(8)]
board_groups = [BoardGroup(i+1, list(range(i*3+1, i*3+4))) for i in range(7)]
ftables = [t for t in tables if t.isplayable]

howell_7rounds_4tables = MovementStrategy([(
    [((ftables[0], Position.NS), (ftables[0], Position.NS)), 
     ((ftables[0], Position.EW), (ftables[3], Position.NS)),
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
movement.autogenerate_initial_sitting()
movement.autogenerate_initial_boardgroup_placement()
print('initial_sitting:')
for tbl, sit in movement.initial_sitting.items():
    print(tbl, sit)
print('initial_board_placement:')
for tbl, bg in movement.initial_boardgroup_placement.items():
    print(tbl, bg)
movement.construct_movement(2)
print('\nround_data[1]:')
for tbl, (sit, bg) in movement.round_data[1].items():
    print(tbl, sit, bg)
print('\nround_data[2]:')
for tbl, (sit, bg) in movement.round_data[2].items():
    print(tbl, sit, bg)
