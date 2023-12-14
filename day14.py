def to_north(grid: list):
	for row in range(1, len(grid)):
		for col in range(0, len(grid[row])):
			if grid[row][col] == 'O':
				i = 1
				while row - i >= 0 and grid[row - i][col] == '.':
					i += 1
				if i > 1:
					grid[row][col] = '.'
					grid[row - i + 1][col] = 'O'

def to_west(grid: list):
	for row in range(0, len(grid)):
		for col in range(1, len(grid[row])):
			if grid[row][col] == 'O':
				i = 1
				while col - i >= 0 and grid[row][col - i] == '.':
					i += 1
				if i > 1:
					grid[row][col] = '.'
					grid[row][col - i + 1] = 'O'

def to_south(grid: list):
	for row in range(len(grid) - 2, -1, -1):
		for col in range(len(grid[row]) - 1, -1, -1):
			if grid[row][col] == 'O':
				i = 1
				while row + i < len(grid) and grid[row + i][col] == '.':
					i += 1
				if i > 1:
					grid[row][col] = '.'
					grid[row + i - 1][col] = 'O'

def to_east(grid: list):
	for row in range(len(grid) - 1, -1, -1):
		for col in range(len(grid[row]) - 2, -1, -1):
			if grid[row][col] == 'O':
				i = 1
				while col + i < len(grid[row]) and grid[row][col + i] == '.':
					i += 1
				if i > 1:
					grid[row][col] = '.'
					grid[row][col + i - 1] = 'O'

# calculate total load on north support beams
def get_result(grid: list) -> int:
	res = 0
	for row in range(0, len(grid)):
		for col in range(0, len(grid[row])):
			if grid[row][col] == 'O':
				res += len(grid) - row
	return res

def find_sublist_index(main_list, sublist):
	try:
		index = main_list.index(sublist[0])
		while main_list[index:index + len(sublist)] != sublist:
			index = main_list.index(sublist[0], index + 1)
		return index
	except ValueError:
		return -1

if __name__ == "__main__":
	with open("input/day14.txt") as file:
		grid = file.readlines()

	for row in range(len(grid)):
		grid[row] = grid[row].rstrip()
		grid[row] = list(grid[row])
	
	# part one
	grid_cpy = grid[:]
	to_north(grid_cpy)
	res = get_result(grid_cpy)
	print("part1:", res)

	# part two is done by analysing pattern of result in a smaller scale, 
	# and use math to handle 1000000000
	grid_cpy = grid[:]
	arr = []
	for i in range(300):
		to_north(grid_cpy)
		to_west(grid_cpy)
		to_south(grid_cpy)
		to_east(grid_cpy)
		res = get_result(grid_cpy)
		arr.append(res)
		# print(i, "|", res)
	
	# based on print result, a loop is found
	loop = [89133, 89106, 89078, 89047, 89048, 89048, 89044, 89049, 89058, 
			89089, 89119, 89150, 89173, 89170, 89171, 89167, 89160]

	index = find_sublist_index(arr, loop)
	
	final_res = loop[(1000000000 - 1 - index) % len(loop)]
	print("part2:", final_res)
