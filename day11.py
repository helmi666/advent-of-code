# assign every galaxy a unique number (id)
# save galaxy id and its coordinates to a dictionary
def sort_galaxies(grid: list) -> dict:
	counter = 0
	galaxies = {}
	for row in range(len(grid)):
		row_data = grid[row]
		for col in range(len(row_data)):
			if row_data[col] == '#':
				counter += 1
				galaxies[counter] = row, col

	return galaxies

# update coordinates of each galaxy based on expansion rate of universe
def update_coords(empty_rows: list, empty_cols: list, galaxies: dict, expansion_rate: int):
	for galaxy_id, coords in galaxies.items():
		row = coords[0]
		col = coords[1]
		counter_r = 0
		for r in empty_rows:
			if r < row:
				counter_r += 1
		counter_c = 0
		for c in empty_cols:
			if c < col:
				counter_c += 1
		new_row = row + counter_r * (expansion_rate - 1)
		new_col = col + counter_c * (expansion_rate - 1)
		galaxies[galaxy_id] = new_row, new_col

# calculate sum of lengths of each unique pair of galaxies
def get_result(galaxies: dict) -> int:
	lengths = 0
	for i in range(1, len(galaxies) + 1):
		for j in range(i + 1, len(galaxies) + 1):
			lengths += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])

	return lengths

if __name__ == "__main__":
	with open("input/day11.txt") as file:
		data = file.readlines()

	grid = [list(row.rstrip()) for row in data]

	# get indices of empty rows and cols
	empty_rows = []
	for row_index, row in enumerate(grid):
		if '#' not in row:
			empty_rows.append(row_index)
	empty_cols = []
	for col_index in range(len(grid[0])):
		if '#' not in [row[col_index] for row in grid]:
			empty_cols.append(col_index)
	
	galaxies = sort_galaxies(grid)
	update_coords(empty_rows, empty_cols, galaxies, 2)
	print(f"part1: {get_result(galaxies)}")

	galaxies = sort_galaxies(grid)
	update_coords(empty_rows, empty_cols, galaxies, 1000000)
	print(f"part2: {get_result(galaxies)}")
