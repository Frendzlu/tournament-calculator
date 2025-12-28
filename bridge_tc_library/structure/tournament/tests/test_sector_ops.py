import pytest

from bridge_tc_library.structure.tournament.sector import Sector


def test_non_destructive_add_single_table():
    s = Sector("A")
    s.add_tables(2)
    original = list(s.tables)

    # non-destructive add of a Table instance
    new = s + original[0]
    assert len(s.tables) == 2
    assert len(new.tables) == 3

    # original table still belongs to source
    assert original[0] in s.tables

    # ensure the added table in the new sector is a distinct object
    assert any(t.table_id == original[0].table_id and t is not original[0] for t in new.tables)


def test_non_destructive_add_list():
    s = Sector("A")
    s.add_tables(5)
    items = [s.tables[1], s.tables[4]]

    out = s + items
    assert len(s.tables) == 5
    assert len(out.tables) == 7


def test_inplace_subtraction():
    s = Sector("A")
    s.add_tables(4)
    ids_before = [t.table_id for t in s.tables]

    s -= [s.tables[0], s.tables[1]]
    assert len(s.tables) == 2
    assert [t.table_id for t in s.tables] == ids_before[2:]


def test_inplace_add_from_other_sector():
    a = Sector("A")
    a.add_tables(2)
    b = Sector("B")
    b.add_tables(2)

    t = b.tables[0]
    a += t
    assert len(a.tables) == 3
    assert len(b.tables) == 1
    assert t.sector is a


def test_non_destructive_subtraction():
    s = Sector("A")
    s.add_tables(3)
    to_remove = s.tables[1]

    out = s - to_remove
    assert len(s.tables) == 3
    assert len(out.tables) == 2
    assert all(t.table_id != to_remove.table_id for t in out.tables)
