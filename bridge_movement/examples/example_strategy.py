from bridge_movement.movements.strategy import MovementStrategy
from bridge_movement.core import Position, Pair, BoardGroup, Player
from bridge_movement.movements.movement import BaseMovement
from typing import Dict
from bridge_movement.tournament import Table, Sector


if __name__ == '__main__':
    # Example usage of BaseMovement with MovementStrategy
    sector = Sector('Example Sector')
    tables = [Table(i + 1, sector) for i in range(5)]  # 5 tables
    pairs = [Pair(i + 1, (Player(f"Player {2*i+1}"), Player(f"Player {2*i+2}"))) for i in range(10)]  # 10 pairs
    board_groups = [BoardGroup(i+1, list(range(i*2+1, i*2+3))) for i in range(5)]  # 5 board group with 2 boards each


    # Define a simple movement strategy
    movement_strategy = MovementStrategy([(
        [((tables[0], Position.NS), (tables[0], Position.NS)), 
         ((tables[0], Position.EW), (tables[1], Position.EW)),
         ((tables[1], Position.NS), (tables[1], Position.NS)),
         ((tables[1], Position.EW), (tables[2], Position.EW)),
         ((tables[2], Position.NS), (tables[2], Position.NS)),
         ((tables[2], Position.EW), (tables[3], Position.EW)),
         ((tables[3], Position.NS), (tables[3], Position.NS)),
         ((tables[3], Position.EW), (tables[4], Position.EW)),
         ((tables[4], Position.NS), (tables[4], Position.NS)),
         ((tables[4], Position.EW), (tables[0], Position.EW)),        
        ],
        [(tables[0], tables[4]),
         (tables[1], tables[0]),
         (tables[2], tables[1]),
         (tables[3], tables[2]),
         (tables[4], tables[3])],
        [1, 2, 3, 4, 5]
    )])

    movement = BaseMovement(tables=tables, board_groups=board_groups, pairs=pairs, movement_strategies=movement_strategy)

    # Example: Get sitting and boards for round 2
    sitting_round_2: Dict[Table, Dict[Position, Pair]] = movement.get_sitting_for_round(2)
    boards_round_2: Dict[Table, BoardGroup] = movement.get_boards_for_round(2)

    print("Sitting for Round 2:")
    for table, positions in sitting_round_2.items():
        print(f"Table {table.table_id}: NS={positions[Position.NS]}, EW={positions[Position.EW]}")

    print("\nBoards for Round 2:")
    for table, board_group in boards_round_2.items():
        print(f"Table {table.table_id}: Board Group={board_group.name}")

