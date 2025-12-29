from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
	first_name: str = ""
	last_name: str = ""
	wk: float = 0.0
	db_id: int = 0
