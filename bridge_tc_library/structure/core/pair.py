from dataclasses import dataclass
from typing import Tuple
from .player import Player

@dataclass(frozen=True)
class Pair:
	id: int
	players: Tuple[Player, Player]

	def __str__(self):
		return str(self.id)