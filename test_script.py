from bridge_tc_library.structure.tournament.sector import Sector


def example():
	"""Simple example showing in-place vs non-destructive operations."""
	sectorA = Sector("A")
	sectorA.add_tables(3)

	sectorB = Sector("B")
	sectorB.add_tables(2)

	print("Initial:")
	print("\tsectorA:", [str(t) for t in sectorA.tables])
	print("\tsectorB:", [str(t) for t in sectorB.tables])

	# in-place: move a table from B into A
	sectorA += sectorB.tables[0]
	print("After in-place add (sectorA += sectorB.tables[0]):")
	print("\tsectorA:", [str(t) for t in sectorA.tables])
	print("\tsectorB:", [str(t) for t in sectorB.tables])

	# non-destructive: create a new sector with an extra table
	sectorC = sectorA + sectorA.tables[0]
	print("Non-destructive add (sectorC = sectorA + table):")
	print("\tsectorA:", [str(t) for t in sectorA.tables])
	print("\tsectorC:", [str(t) for t in sectorC.tables])


if __name__ == "__main__":
	example()