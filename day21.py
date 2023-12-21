from collections import deque

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
	
	queue = deque([(len(grid) // 2, len(grid[0]) // 2)])
	counter = 0
	rounds = 0
	tasks_add = 1
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
		if counter == tasks_add:
			tasks_add = len(queue)
			rounds += 1
			counter = 0
		if rounds == 64:
			break
	
	print("part1:", len(queue))
