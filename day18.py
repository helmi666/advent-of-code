def get_coords(instruction: list) -> tuple:
	rows = []
	cols = []
	r, c = 0, 0
	for row in instruction:
		if row[0] == 'R':
			c += row[1]
		if row[0] == 'D':
			r += row[1]
		if row[0] == 'L':
			c -= row[1]
		if row[0] == 'U':
			r -= row[1]
		rows.append(r)
		cols.append(c)
	return rows, cols

def get_edge_len(instruction: list) -> int:
	counter = 0
	for row in instruction:
		for i in range(1, row[1] + 1):
			counter += 1
	return counter

def get_area(coords):
	rows = coords[0]
	cols = coords[1]

	count = 0
	for r, c in zip(rows, cols[1:] + [cols[0]]):
		count += r * c
	for r, c in zip(rows[1:] + [rows[0]], cols):
		count -= r * c
	area = 0.5 * abs(count)

	return area

if __name__ == "__main__":
	with open("input/day18.txt") as file:
		data = file.read().splitlines()

	data = [line.split() for line in data]
	data = [[line[0], int(line[1]), line[2]] for line in data]

	# part one
	coords = get_coords(data)
	# use shoelace formula to calculate polygon area as
	# coordinates of its vertices are known
	area1 = get_area(coords)
	# from above we get twisted area (based on coords - center of the tiles) which
	# does not represent the whole area as required in this puzzle <- edge tiles + interior tiles
	# for each edge tile 1/2 of itself should be added plus 1 (sum of all corner tiles)
	area2 = get_edge_len(data) / 2 + 1
	print("part1:", area1 + area2)

	# part two
	new_data = []
	for row in data:
		new_row = []
		dirct = row[2][-2]
		if dirct == '0':
			new_row.append('R')
		if dirct == '1':
			new_row.append('D')
		if dirct == '2':
			new_row.append('L')
		if dirct == '3':
			new_row.append('U')
		dist = int(''.join(list(row[2])[2:7]), 16)
		new_row.append(dist)
		new_data.append(new_row)
	
	new_coords = get_coords(new_data)
	area1 = get_area(new_coords)
	area2 = get_edge_len(new_data) / 2 + 1
	print("part2:", area1 + area2)
