from collections import deque

def energized(grid: list, queue: list) -> int:
		# a dict to keep track of visited tile plus the entering dirct: key=(row, col), value=[dirct1, dirct2...]
		visited = {}
		while queue:
			r, c, d = queue.popleft()
			r += dircts[d][0]
			c += dircts[d][1]
			# if target tile is within boundaries of grid
			if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
				if (r, c) not in visited.keys():
					visited[(r, c)] = []
				if (r, c) in visited.keys() and d in visited[(r, c)]:
					continue
				visited[(r, c)].append(d)
				tile = grid[r][c]
				next_dirct = turns[tile][d]
				for i in range(len(next_dirct)):
					next_move = r, c, next_dirct[i]
					queue.append(next_move)
		# uncomment the following to visualize the visited tiles: '#' for visited/energized '.' otherwise
		""" coords = list(visited.keys())
		for r, row in enumerate(grid):
			for c, col in enumerate(grid[0]):
				if (r, c) in coords:
					print("X", end="")
				else:
					print(".", end="")
			print() """
		return len(visited)

if __name__ == "__main__":
	with open("input/day16.txt") as file:
		grid = file.readlines()

	for row in range(len(grid)):
		grid[row] = grid[row].rstrip()
		grid[row] = list(grid[row])
	
	# change of coordinates (row, col) based on four directions: right(indexed 0), down(1), left(2), up(3)
	dircts = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	
	# turns depends on what is encountered:
	# next dirct based on prev dirct + tile('.', '/', '\\', '|', '-')
	turns = {
		'.': ((0, ), (1, ), (2, ), (3, )),
		'/': ((3, ), (2, ), (1, ), (0, )), 
		'\\': ((1, ), (0, ), (3, ), (2, )), 
		'|': ((1, 3), (1, ), (1, 3), (3, )),
		'-': ((0, ), (0, 2), (2, ), (0, 2))
	}

	# part one
	# a tuple of (row, column, direction) to keep track of each move
	queue = deque([(0, -1, 0)])
	print("part1:", energized(grid, queue))

	# part two
	queues = []
	for row in range(len(grid)):
		queue = deque([(row, -1, 0)])
		queues.append(queue)
	for col in range(len(grid[0])):
		queue = deque([(-1, col, 1)])
		queues.append(queue)
	for row in range(len(grid)):
		queue = deque([(row, len(grid[0]), 2)])
		queues.append(queue)
	for col in range(len(grid[0])):
		queue = deque([(len(grid), col, 3)])
		queues.append(queue)
	counter = []
	for queue in queues:
		counter.append(energized(grid, queue))
	print("part2:", max(counter))
