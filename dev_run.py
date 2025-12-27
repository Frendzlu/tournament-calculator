from bridge_movement.movements.mitchell import MitchellMovement
from bridge_movement.movements.board_group_movement import BoardGroupMovement

m = MitchellMovement(8)
print('Mitchell num_tables =', m.num_tables)
print('pair_rounds count =', len(m.pair_rounds))
print('pair_rounds[1] sample =', m.pair_rounds[0])

bg = BoardGroupMovement(num_boards=16, num_tables=m.num_tables)
print('Board groups:', [g.boards for g in bg.groups])
print('First_Boards r1:', bg.first_board_for_round(1))
print('Boards for r1:', bg.boards_for_round(1))
print('Board groups ids for r1:', bg.board_group_ids_for_round(1))
print('First_Boards r2:', bg.first_board_for_round(2))
print('Boards for r2:', bg.boards_for_round(2))
print('Board groups ids for r2:', bg.board_group_ids_for_round(2))
print('Movement r1->r2:', bg.board_group_movement_between(1,2))

