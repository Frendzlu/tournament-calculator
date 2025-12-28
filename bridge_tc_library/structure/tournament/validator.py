from collections import defaultdict

class ValidationEngine:
	def __init__(self):
		self.pair_boards = defaultdict(set)
		self.pair_opponents = defaultdict(set)

	def validate_round(self, pairs_round, boards_round):
		table_map = {}

		for (table, pos), pair in pairs_round.items():
			table_map.setdefault(table, {})[pos] = pair

		for table, positions in table_map.items():
			ns = positions["NS"]
			ew = positions["EW"]
			board_group = boards_round[table]

			for board in board_group.boards:
				if board in self.pair_boards[ns]:
					raise ValueError(f"{ns.id} replayed board {board}")
				if board in self.pair_boards[ew]:
					raise ValueError(f"{ew.id} replayed board {board}")

				self.pair_boards[ns].add(board)
				self.pair_boards[ew].add(board)

			if ew in self.pair_opponents[ns]:
				raise ValueError(f"{ns.id} vs {ew.id} repeated")

			self.pair_opponents[ns].add(ew)
			self.pair_opponents[ew].add(ns)
