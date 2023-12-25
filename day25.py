import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
	with open("input/day25.txt") as file:
		data = file.read().splitlines()

	components = []
	for line in data:
		item0, items_str = line.split(": ")
		items = items_str.split()
		for item in items:
			if not any((item0, item) in pair or (item, item0) in pair for pair in components):
				components.append((item0, item))

	G = nx.Graph()
	G.add_edges_from(components)
	cut_edges = nx.minimum_edge_cut(G)
	G.remove_edges_from(cut_edges)

	# uncomment the following to visualize the graph
	""" degree_color = [G.degree(node) for node in G.nodes()]
	pos = nx.spring_layout(G)
	plt.figure(figsize=(10, 8))
	nx.draw(G, pos, node_size=25, node_color=degree_color, cmap=plt.cm.Blues, edge_color='#FFD580', alpha=0.7)
	plt.title("Components")
	plt.show() """

	group1, group2 = list(nx.connected_components(G))
	print(len(group1) * len(group2))
