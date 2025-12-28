from typing import Any, Dict, Optional

from bridge_tc_library.structure.tournament import Tournament


class BWSLiveClient:
    """Minimal BWS client abstraction.

    Responsibilities:
    - create an initial BWS representation from a validated `Tournament`
    - apply incremental updates when the tournament changes
    - persist/load BWS representation to/from storage

    The concrete representation used here is intentionally generic (`Dict`) so
    projects integrating with a real BWS format can adapt easily.
    """

    def __init__(self) -> None:
        self._bws: Optional[Dict[str, Any]] = None

    def create_bws_from_tournament(self, tournament: Tournament) -> Dict[str, Any]:
        """Build an initial BWS-like structure from `Tournament`.

        This function must be called only after the `tournament` has been
        validated for feasibility by the core movement/tournament module.
        """
        # Minimal example structure: mapping table_id -> (ns_pair_id, ew_pair_id, boards)
        bws = {
            "tournament_name": getattr(tournament, "name", ""),
            "tables": {}
        }
        for t in getattr(tournament, "tables", []):
            bws["tables"][t.table_id] = {
                "ns": getattr(getattr(t, "current_pairs", {}), "get", lambda k: None)("NS"),
                "ew": getattr(getattr(t, "current_pairs", {}), "get", lambda k: None)("EW"),
                "board_group": getattr(t, "current_board_set", None)
            }
        self._bws = bws
        return bws

    def update_from_tournament(self, tournament: Tournament) -> Dict[str, Any]:
        """Apply an in-memory update from a tournament that has changed.

        Implementations can choose to compute deltas or rebuild the structure.
        """
        if self._bws is None:
            return self.create_bws_from_tournament(tournament)
        # naive full rebuild for now
        return self.create_bws_from_tournament(tournament)

    def save(self, path: str) -> None:
        """Persist the in-memory BWS representation to a file (JSON for now)."""
        import json

        if self._bws is None:
            raise RuntimeError("No BWS data to save")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self._bws, fh, default=str, indent=2)

    def load(self, path: str) -> Dict[str, Any]:
        import json

        with open(path, "r", encoding="utf-8") as fh:
            self._bws = json.load(fh)
        return self._bws
