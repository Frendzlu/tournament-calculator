from bridge_movement.movements.mitchell import MitchellMovement
from bridge_movement.tournament.sector import Sector
from bridge_movement.tournament.table import Table
from bridge_movement.core import Position


def print_round(movement, tables, r):
	print(f"Round {r}")
	sitting = movement.get_round_sitting(r, tables=tables)
	for tbl in tables:
		ns = sitting[tbl][Position.NS]
		ew = sitting[tbl][Position.EW]
		print(f"  Table {tbl.table_id}: NS={ns}  EW={ew}")
	print()


def print_strategy(movement, tables):
	mov = movement.get_movement_strategy(tables=tables)
	print("Movement strategy (per round):")
	for changes, rounds in mov.strategies:
		print(f" Rounds: {rounds}")
		if not changes:
			print("  (no explicit changes)")
		else:
			for (from_tbl, from_pos), (to_tbl, to_pos) in changes:
				from_id = getattr(from_tbl, 'table_id', from_tbl)
				to_id = getattr(to_tbl, 'table_id', to_tbl)
				print(f"  {from_id} {from_pos.value} -> {to_id} {to_pos.value}")
		print()


if __name__ == '__main__':
	# Example: 8 pairs -> 4 tables
	num_pairs = 8
	movement = MitchellMovement(num_pairs=num_pairs)
	sector = Sector('Example')
	tables = [Table(i + 1, sector) for i in range(movement.num_tables)]

	print(f"Mitchell movements example: {movement.num_tables} tables, {len(movement.pair_rounds)} rounds\n")

	# Print all round sittings
	for r in range(1, len(movement.pair_rounds) + 1):
		print_round(movement, tables, r)

	# Print movements strategy (changes between rounds)
	print_strategy(movement, tables)

