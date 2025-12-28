from typing import List, Optional
from .validator import ValidationEngine
from .sector import Sector


class Tournament:
    def __init__(self, total_boards: int) -> None:
        self.total_boards: int = total_boards
        self.sectors: List[Sector] = []
        # separate per-deal counter overall is optional; sectors manage their own within-round idx
        self.validator: ValidationEngine = ValidationEngine()

    def add_sector(self, sector: Sector) -> None:
        self.sectors.append(sector)

    def next_deal(self) -> None:
        """
        Advance the tournament by one deal. This performs validation for the
        single board currently being played in each sector (sectors may be at
        different positions in their rounds).
        Raises StopIteration when no sector remains active.
        """
        # If no active sectors, signal end of tournament
        active: bool = any(
            sector.current_pairs_round is not None and sector.current_boards_round is not None
            for sector in self.sectors
        )
        if not active:
            raise StopIteration

        # Validate per-sector single-board mappings and advance each sector by one deal
        for sector in self.sectors:
            if sector.current_pairs_round is None or sector.current_boards_round is None:
                continue

            for table in sector.tables.values():
                if table.current_board is None:
                    continue

                # Skip validation if the deal is not the last in the board group
                if sector.current_within_round_index < sector.boards_per_round - 1:
                    continue

                # Validate the current one-board-per-table mapping against current pairs
                self.validator.validate_round(
                    {k: v for k, v in sector.current_pairs_round.items() if k[0] == table.table_id},
                    {table.table_id: table.current_board_set},
                )

        # If all validations passed, advance each sector's internal deal index
        for sector in self.sectors:
            if sector.current_pairs_round is None or sector.current_boards_round is None:
                continue
            sector.advance_deal()

    def next_round(self) -> None:
        """
        Advance the tournament to the next full round in each sector.
        This forces sectors to move to their next pairs round and next boards round
        regardless of their current within-round deal index.
        """
        for sector in self.sectors:
            if sector.current_pairs_round is None:
                continue

            # Validate the entire round before advancing
            self.validator.validate_round(
                sector.current_pairs_round,
                sector.current_boards_round,
            )

            # Reset within-round index and advance round
            sector.advance_round()
