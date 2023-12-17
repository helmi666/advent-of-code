# pip install networkx, if module not found
import networkx as nx

class Node:
	nodes = {}

	def __init__(self, coord: tuple, level: int, dirct: str):
		self.coord = coord
		self.level = level
		self.dirct = dirct

	@classmethod
	def get_node(cls, coord: tuple, level: int, dirct: str) -> "Node":
		if not (coord, level, dirct) in Node.nodes:
			Node.nodes[(coord, level, dirct)] = Node(coord, level, dirct)
		return Node.nodes[(coord, level, dirct)]

def straight(G: nx.DiGraph, r: int, c: int, levels1: list, levels2: list):
	for level1, level2 in zip(levels1, levels2):
		# horizontal eastward
		node1 = Node.get_node((r, c - 0.5), level1, "East")
		node2 = Node.get_node((r, c + 0.5), level2, "East")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# horizontal westward
		node1 = Node.get_node((r, c + 0.5), level1, "West")
		node2 = Node.get_node((r, c - 0.5), level2, "West")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# vertical southward
		node1 = Node.get_node((r - 0.5, c), level1, "South")
		node2 = Node.get_node((r + 0.5, c), level2, "South")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# vertical northward
		node1 = Node.get_node((r + 0.5, c), level1, "North")
		node2 = Node.get_node((r - 0.5, c), level2, "North")
		G.add_edge(node1, node2, weight=costs[(r, c)])

def turns(G: nx.DiGraph, r: int, c: int, levels1: list, levels2: list):
	for level1, level2 in zip(levels1, levels2):
		# turn right from west
		node1 = Node.get_node((r, c - 0.5), level1, "East")
		node2 = Node.get_node((r + 0.5, c), level2, "South")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn right from south
		node1 = Node.get_node((r + 0.5, c), level1, "North")
		node2 = Node.get_node((r, c + 0.5), level2, "East")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn right from east
		node1 = Node.get_node((r, c + 0.5), level1, "West")
		node2 = Node.get_node((r - 0.5, c), level2, "North")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn right from north
		node1 = Node.get_node((r - 0.5, c), level1, "South")
		node2 = Node.get_node((r, c - 0.5), level2, "West")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn left from west
		node1 = Node.get_node((r, c - 0.5), level1, "East")
		node2 = Node.get_node((r - 0.5, c), level2, "North")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn left from north
		node1 = Node.get_node((r - 0.5, c), level1, "South")
		node2 = Node.get_node((r, c + 0.5), level2, "East")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn left from east
		node1 = Node.get_node((r, c + 0.5), level1, "West")
		node2 = Node.get_node((r + 0.5, c), level2, "South")
		G.add_edge(node1, node2, weight=costs[(r, c)])

		# turn left from south
		node1 = Node.get_node((r + 0.5, c), level1, "North")
		node2 = Node.get_node((r, c - 0.5), level2, "West")
		G.add_edge(node1, node2, weight=costs[(r, c)])

if __name__ == "__main__":
	with open("input/day17.txt") as file:
		grid = file.readlines()

	for row in range(len(grid)):
		grid[row] = grid[row].rstrip()
		grid[row] = [int(nbr) for nbr in list(grid[row])]

	costs = {}
	for r, row in enumerate(grid):
		for c, cost in enumerate(row):
			costs[(r, c)] = cost

	# create directed graphs part1 and part2
	G1 = nx.DiGraph()
	G2 = nx.DiGraph()

	for r, row in enumerate(grid):
		for c in range(len(row)):
			levels1 = [0, 1]
			levels2 = [1, 2]
			straight(G1, r, c, levels1, levels2)

			levels1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
			levels2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
			straight(G2, r, c, levels1, levels2)

			levels1 = [0, 1, 2]
			levels2 = [0, 0, 0]
			turns(G1, r, c, levels1, levels2)

			levels1 = [3, 4, 5, 6, 7, 8, 9]
			levels2 = [0, 0, 0, 0, 0, 0, 0]
			turns(G2, r, c, levels1, levels2)

	# connect first node to graph (part1+2)
	node1 = Node.get_node((0, 0), 0, "None")
	node2 = Node.get_node((0, 0.5), 0, "East")
	G1.add_edge(node1, node2, weight=0)
	G2.add_edge(node1, node2, weight=0)

	node1 = Node.get_node((0, 0), 0, "None")
	node2 = Node.get_node((0.5, 0), 0, "South")
	G1.add_edge(node1, node2, weight=0)
	G2.add_edge(node1, node2, weight=0)

	# connect last node to graph (part1)
	levels1 = [0, 1, 2]
	levels2 = [3, 3, 3]
	f_row = len(grid) - 1
	f_col = len(grid[0]) - 1
	for level1, level2 in zip(levels1, levels2):
		node1 = Node.get_node((f_row, f_col - 0.5), level1, "East")
		node2 = Node.get_node((f_row, f_col), level2, "None")
		G1.add_edge(node1, node2, weight=costs[f_row, f_col])

		node1 = Node.get_node((f_row - 0.5, f_col), level1, "South")
		node2 = Node.get_node((f_row, f_col), level2, "None")
		G1.add_edge(node1, node2, weight=costs[f_row, f_col])

	# connect last node to graph (part2)
	levels1 = [3, 4, 5, 6, 7, 8, 9]
	levels2 = [10, 10, 10, 10, 10, 10, 10]
	for level1, level2 in zip(levels1, levels2):
		node1 = Node.get_node((f_row, f_col - 0.5), level1, "East")
		node2 = Node.get_node((f_row, f_col), level2, "None")
		G2.add_edge(node1, node2, weight=costs[f_row, f_col])

		node1 = Node.get_node((f_row - 0.5, f_col), level1, "South")
		node2 = Node.get_node((f_row, f_col), level2, "None")
		G2.add_edge(node1, node2, weight=costs[f_row, f_col])

	# specify source and destination nodes
	src = Node.get_node((0, 0), 0, "None")
	dest_p1 = Node.get_node((f_row, f_col), 3, "None")
	dest_p2 = Node.get_node((f_row, f_col), 10, "None")

	# get least heat loss
	least_heat_loss_part1 = nx.shortest_path_length(G1, source=src, target=dest_p1, weight='weight')
	least_heat_loss_part2 = nx.shortest_path_length(G2, source=src, target=dest_p2, weight='weight')
	print(f"part1: {least_heat_loss_part1}")
	print(f"part2: {least_heat_loss_part2}")
