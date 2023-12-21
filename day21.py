from collections import deque
import numpy as np

# improved efficiency for part2
def bfs(grid: list, coords: dict, steps_count: int) -> int:
	row_len = len(grid)
	col_len = len(grid[0])
	queue = deque([(len(grid) // 2, len(grid[0]) // 2, 0)])
	visited = set()
	dircts = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	while queue:
		r, c, steps = queue.popleft()
		if steps > steps_count:
			continue
		for dr, dc in dircts:
			new_r, new_c = r + dr, c + dc
			# % row_len/col_len to project infinite grid for part2
			if coords[(new_r % row_len, new_c % col_len)] != '#' and (new_r, new_c) not in visited:
				visited.add((new_r, new_c))
				queue.append((new_r, new_c, steps + 1))
	# each step/round -> r+c increases by one, odd steps -> odd r+c, even steps -> even r+c
	return len([(r, c) for (r, c) in visited if (r + c) % 2 == steps_count % 2])

if __name__ == "__main__":
	with open("input/day21.txt") as file:
		grid = file.readlines()

	for row in range(len(grid)):
		grid[row] = grid[row].rstrip()
		grid[row] = list(grid[row])

	coords = {}
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			coords[(r, c)] = col

	# part one
	# slow bfs as backtracking is included, but works for part1
	queue = deque([(len(grid) // 2, len(grid[0]) // 2)])
	counter = 0
	rounds = 0
	tasks_added = 1
	while queue:
		r, c = queue.popleft()
		if r + 1 < len(grid):
			if coords[(r + 1, c)] != '#' and not (r + 1, c) in queue:
				queue.append((r + 1, c))
		if c + 1 < len(grid[0]):
			if coords[(r, c + 1)] != '#' and not (r, c + 1) in queue:
				queue.append((r, c + 1))
		if r - 1 >= 0:
			if coords[(r - 1, c)] != '#' and not (r - 1, c) in queue:
				queue.append((r - 1, c))
		if c - 1 >= 0:
			if coords[(r, c - 1)] != '#' and not (r, c - 1) in queue:
				queue.append((r, c - 1))
		counter += 1
		if counter == tasks_added:
			tasks_added = len(queue)
			rounds += 1
			counter = 0
		if rounds == 64:
			break

	print("part1:", len(queue))

	# part two
	# 131 is the width/height of the grid; no obstacles from S to edges at four sides 
	# 26501365 = 65 + 131 * 202300, which means in addition to traversing the original 
	# grid from S, 202300 times of the expanded grid is traversed
	x_values = [0, 1, 2, 3, 4, 5]
	# 65, 196, 327, 458, 589, 720 -> 
	# 65 + 131 * 0, 65 + 131 * 1, 65 + 131 * 2, 65 + 131 * 3, 65 + 131 * 4, 65 + 131 * 5
	y_values = [bfs(grid, coords, steps_count) for steps_count in [65, 196, 327, 458, 589, 720]]
	# fitting a polynomial of degree 2 (quadratic) to the data
	coefficients = np.polyfit(x_values, y_values, 2)
	res = np.polyval(coefficients, 202300)
	print("part2:", np.round(res, 0))
