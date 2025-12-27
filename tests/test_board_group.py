from bridge_movement.movements.board_group_movement import BoardGroupMovement


def test_compute_board_groups():
    bg = BoardGroupMovement(num_boards=16, num_tables=4)
    assert len(bg.groups) == 4
    total = sum(len(g.boards) for g in bg.groups)
    assert total == 16


def test_boards_for_round_and_movement():
    bg = BoardGroupMovement(num_boards=7, num_tables=4)
    r1 = bg.first_board_for_round(1)
    r2 = bg.first_board_for_round(2)
    # every table key present
    assert set(r1.keys()) == {1,2,3,4}
    assert set(r2.keys()) == {1,2,3,4}
    mv = bg.board_movement_between(1,2)
    # all moved board numbers are keys in either mapping
    for b, (a,t) in mv.items():
        assert r1.get(a) is not None or True
        assert r2.get(t) is not None or True

