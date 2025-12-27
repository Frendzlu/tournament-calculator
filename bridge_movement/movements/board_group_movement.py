from typing import List, Dict, Tuple
from bridge_movement.core import BoardGroup


class BoardGroupMovement:
    """Compute board-group assignments and board movement between rounds.

    - BoardGroups are computed as contiguous ranges of board numbers divided among tables.
    - boards_for_round(round_index) returns a mapping table_index -> board_number for that round.
    - board_movement_between(a, b) returns mapping board_number -> (from_table, to_table).

    Indexing: tables are 1-based (table 1..num_tables). Boards are 1-based.
    """

    def __init__(self, num_boards: int, num_tables: int, group_size: int = None):
        if num_tables <= 0:
            raise ValueError("num_tables must be > 0")
        if num_boards <= 0:
            raise ValueError("num_boards must be > 0")
        self.num_boards = num_boards
        self.num_tables = num_tables
        self.group_size = group_size
        # compute groups at init
        self.groups = self.compute_board_groups()

    def compute_board_groups(self) -> List[BoardGroup]:
        # default group size: floor division distributing remainder to earlier groups
        if self.group_size is None:
            base = self.num_boards // self.num_tables
            rem = self.num_boards % self.num_tables
            sizes = [(base + (1 if i < rem else 0)) for i in range(self.num_tables)]
        else:
            # group_size explicitly provided
            sizes = []
            remaining = self.num_boards
            while remaining > 0:
                sizes.append(min(self.group_size, remaining))
                remaining -= self.group_size
            # if sizes fewer than tables, pad with empty
            if len(sizes) < self.num_tables:
                sizes += [0] * (self.num_tables - len(sizes))
        groups: List[BoardGroup] = []
        cur = 1
        for idx in sizes:
            if idx <= 0:
                groups.append(BoardGroup(int, tuple()))
                continue
            boards = tuple(range(cur, cur + idx))
            groups.append(BoardGroup(idx, boards))
            cur += idx
        return groups

    def first_board_for_round(self, round_index: int) -> Dict[int, int]:
        """Return mapping table_index->board for given round_index (1-based rounds).

        Default behavior: for round r, the table i plays group index ((i-1 + (r-1)) % n_groups).
        i.e. every round groups rotate downward by 1.
        """
        if round_index < 1:
            raise ValueError("round_index must be >= 1")
        n = len(self.groups)
        out: Dict[int, int] = {}
        # pick the first board in the group's tuple as representative for the table
        for i in range(1, self.num_tables + 1):
            group_idx = (i - 1 + (round_index - 1)) % n
            group = self.groups[group_idx]
            board = group.boards[0] if len(group.boards) > 0 else None
            out[i] = board
        return out

    def boards_for_round(self, round_index: int) -> Dict[int, Tuple[int, ...]]:
        """Return mapping table_index->boards for given round_index (1-based rounds).
        """
        if round_index < 1:
            raise ValueError("round_index must be >= 1")
        n = len(self.groups)
        out: Dict[int, Tuple[int, ...]] = {}
        for i in range(1, self.num_tables + 1):
            group_idx = (i - 1 + (round_index - 1)) % n
            group = self.groups[group_idx]
            out[i] = group.boards
        return out

    def board_group_id_for_round(self, round_index: int) -> Dict[int, int]:
        """Return mapping table_index->board_group_id for given round_index (1-based rounds).
        """
        if round_index < 1:
            raise ValueError("round_index must be >= 1")
        n = len(self.groups)
        out: Dict[int, int] = {}
        for i in range(1, self.num_tables + 1):
            group_idx = (i - 1 + (round_index - 1)) % n
            group = self.groups[group_idx]
            out[i] = group.BoardGroupId
        return out
#this should be returning Board group movements, not individual boards. Mateusz tell me what you think
    def board_group_movement_between(self, round_a: int, round_b: int) -> Dict[int, Tuple[int, int]]:
        """Return mapping board_group_id -> (from_table, to_table) between two rounds.

        If a board_group is not present on any table (e.g. groups shorter than num_tables), it will be omitted.
        """
        a_map = self.board_group_id_for_round(round_a)
        b_map = self.board_group_id_for_round(round_b)
        inv_a: Dict[int, int] = {b: t for t, b in a_map.items() if b is not None}
        inv_b: Dict[int, int] = {b: t for t, b in b_map.items() if b is not None}
        movement: Dict[int, Tuple[int, int]] = {}
        for board_group_id, from_table in inv_a.items():
            to_table = inv_b.get(board_group_id, None)
            if to_table is not None:
                movement[board_group_id] = (from_table, to_table)
        return movement

