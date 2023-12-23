import networkx as nx
from collections import deque

if __name__ == "__main__":
	with open("input/day23.txt") as file:
		grid = file.read().splitlines()

	grid = [list(row) for row in grid]
	max_row = len(grid)
	max_col = len(grid[0])

	contents = {}
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			contents[(r, c)] = col

	start = (0, 1)
	goal = (max_row - 1, max_col -2)

	# part one
	# directed graph for part1
	G1 = nx.DiGraph()
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			if col == '.':
				# check right
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
						G1.add_edge((next_r, next_c), (r, c), weight=1)
					elif contents[(next_r, next_c)] == '>':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
					elif contents[(next_r, next_c)] == '<':
						G1.add_edge((next_r, next_c), (r, c), weight=1)
				# check down
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
						G1.add_edge((next_r, next_c), (r, c), weight=1)
					elif contents[(next_r, next_c)] == 'v':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
					elif contents[(next_r, next_c)] == '^':
						G1.add_edge((next_r, next_c), (r, c), weight=1)
			elif col == '>':
				# check right
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.' or contents[(next_r, next_c)] == '>':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == 'v':
				# check down
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.' or contents[(next_r, next_c)] == 'v':
						G1.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == '<':
				# check right
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.' or contents[(next_r, next_c)] == '<':
						G1.add_edge((next_r, next_c), (r, c), weight=1)
			elif col == '^':
				# check down
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] == '.' or contents[(next_r, next_c)] == '^':
						G1.add_edge((next_r, next_c), (r, c), weight=1)

	# generate all simple paths in graph between two specified nodes
	# a simple path -> a path in which no node appears more than once
	all_paths = nx.all_simple_edge_paths(G1, start, goal)
	all_paths_lens = map(len, all_paths)
	print("part1:", max(all_paths_lens))

	# part2 (takes approx. one minute to get the result)
	# undirected graph for part2
	G2 = nx.Graph()
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			if col == '.':
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".><":
						G2.add_edge((r, c), (next_r, next_c), weight=1)
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".v^":
						G2.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == '>':
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".><":
						G2.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == 'v':
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".v^":
						G2.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == '<':
				next_r, next_c = r, c + 1
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".><":
						G2.add_edge((r, c), (next_r, next_c), weight=1)
			elif col == '^':
				next_r, next_c = r + 1, c
				if 0 <= next_r < max_row and 0 <= next_c < max_col:
					if contents[(next_r, next_c)] in ".v^":
						G2.add_edge((r, c), (next_r, next_c), weight=1)

	# intersections -> a node that has more than 2 neighbors
	# introduced as G2 is not sufficient to produce result
	# another graph (G3) will be created in which each node is represented by intersections
	intersections = [start]
	for node in G2.nodes:
		if len(G2.edges(node)) > 2:
			intersections.append(node)
	intersections.append(goal)

	def reachable_intersections(grid: list, start: tuple, intersections: list) -> dict:
		# key = all intersections that start can reach
		# value = distance between start and corresponding intersection
		distances = {}
		visited = set()
		queue = deque([(start, 0)])
		while queue:
			node, dist = queue.popleft()
			# record intersection and distance between start and this intersection
			if node in intersections and node != start:
				distances[node] = dist
				continue
			for neighbor in list(G2.neighbors(node)):
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append((neighbor, dist + 1))
		return {start: distances}

	G3 = nx.Graph()
	visited = set()
	for node in intersections:
		node_to_next = reachable_intersections(grid, node, intersections)
		reachable = node_to_next[node]
		for r in reachable:
			if r not in visited:
				visited.add((node, r))
				G3.add_edge(node, r, weight=reachable[r])

	all_paths = nx.all_simple_edge_paths(G3, start, goal)

	def path_length(path: list) -> int:
		length = 0
		for nodes in path:
			length += G3.get_edge_data(nodes[0], nodes[1])['weight']
		return length

	all_paths_lens = map(path_length, all_paths)
	print("part2:", max(all_paths_lens))
