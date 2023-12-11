""" part one """

class Tile:
	def __init__(self, value: str, pos: tuple):
		self.value = value
		self.pos = pos
	
	def s_next(self, grid: list) -> "Tile":
		if self.pos[1] - 1 >= 0:
			next_pos = (self.pos[0], self.pos[1] - 1)
			next = Tile(find_value(grid, next_pos), next_pos)
			if next.value in ['F', '-', 'L']:
				return next
		if self.pos[0] - 1 >= 0:
			next_pos = (self.pos[0] - 1, self.pos[1])
			next = Tile(find_value(grid, next_pos), next_pos)
			if next.value in ['7', '|', 'F']:
				return next
		if self.pos[1] + 1 < len(grid[0]):
			next_pos = (self.pos[0], self.pos[1] + 1)
			next = Tile(find_value(grid, next_pos), next_pos)
			if next.value in ['J', '-', '7']:
				return next
		if self.pos[1] + 1 < len(grid):
			next_pos = (self.pos[0] + 1, self.pos[1])
			next = Tile(find_value(grid, next_pos), next_pos)
			if next.value in ['J', '|', 'L']:
				return next
	
	def vp_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[0] > prev.pos[0]:
			row = self.pos[0] + 1
		else:
			row = self.pos[0] - 1
		next_pos = row, self.pos[1]
		return Tile(find_value(grid, next_pos), next_pos)

	def hp_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[1] > prev.pos[1]:
			col = self.pos[1] + 1
		else:
			col = self.pos[1] - 1
		next_pos = self.pos[0], col
		return Tile(find_value(grid, next_pos), next_pos)

	def l_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[0] == prev.pos[0]:
			next_pos = self.pos[0] - 1, self.pos[1]
		else:
			next_pos = self.pos[0], self.pos[1] + 1
		return Tile(find_value(grid, next_pos), next_pos)
	
	def j_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[0] == prev.pos[0]:
			next_pos = self.pos[0] - 1, self.pos[1]
		else:
			next_pos = self.pos[0], self.pos[1] - 1
		return Tile(find_value(grid, next_pos), next_pos)
	
	def seven_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[0] == prev.pos[0]:
			next_pos = self.pos[0] + 1, self.pos[1]
		else:
			next_pos = self.pos[0], self.pos[1] - 1
		return Tile(find_value(grid, next_pos), next_pos)
	
	def f_next(self, grid: list, prev: "Tile") -> "Tile":
		if self.pos[0] == prev.pos[0]:
			next_pos = self.pos[0] + 1, self.pos[1]
		else:
			next_pos = self.pos[0], self.pos[1] + 1
		return Tile(find_value(grid, next_pos), next_pos)

def find_s(grid: list) -> tuple:
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			if grid[row][col] == 'S':
				return row, col

def find_value(grid: list, pos: tuple) -> str:
	for row in range(len(grid)):
		if row == pos[0]:
			for col in range(len(grid[row])):
				if col == pos[1]:
					return grid[row][col]

def find_next(grid: list, current: Tile, prev: Tile) -> Tile:
	if current.value == '|':
		next_tile = current.vp_next(grid, prev)
	if current.value == '-':
		next_tile = current.hp_next(grid, prev)
	if current.value == 'L':
		next_tile = current.l_next(grid, prev)
	if current.value == 'J':
		next_tile = current.j_next(grid, prev)
	if current.value == '7':
		next_tile = current.seven_next(grid, prev)
	if current.value == 'F':
		next_tile = current.f_next(grid, prev)
	return next_tile

# parse data from file into a 2D array (a list of strings)
with open("input/day10.txt") as file:
	grid = file.readlines()

grid = [row.rstrip() for row in grid]

# pipe: list of tiles (instances of the class "Tile")
# first and last element of the list -> S
start_tile = Tile('S', find_s(grid))
next_tile = start_tile.s_next(grid)
pipe = [start_tile, next_tile]

while next_tile.pos != start_tile.pos:
	next_tile = find_next(grid, pipe[-1], pipe[-2])
	pipe.append(next_tile)

print(f"part1: {len(pipe) // 2}")


""" part two """

def is_pipe(current_pos: tuple, pipe: list) -> bool:
	for tile in pipe:
		if current_pos == tile.pos:
			return True
	return False

# uncomment the following to visualize the pipe
""" for row in range(len(grid)):
	for col in range(len(grid[row])):
		if is_pipe((row, col), pipe):
			print('x', end="")
		else:
			print('.', end="")
	print("") """

# get the "value" of S for purpose of counting vertical walls
def get_s_value(pipe: list) -> str:
	if pipe[1].pos[0] == pipe[-2].pos[0]:
		return '-'
	if pipe[1].pos[1] == pipe[-2].pos[1]:
		return '|'
	if pipe[1].pos[1] == pipe[0].pos[1] + 1:
		if pipe[-2].pos[0] == pipe[0].pos[0] + 1:
			return 'F'
		else:
			return 'L'
	if pipe[1].pos[1] == pipe[0].pos[1] - 1:
		if pipe[-2].pos[0] == pipe[0].pos[0] + 1:
			return '7'
		else:
			return 'J'

# check nums of vertical "walls" on the left (or right, but always same row) of a given tile: 
# odd -> in loop, even -> outside loop
# break down further: if sum of upward walls ('|', 'L', 'J') is an odd num -> in loop
# alternatively, if sum of downward walls ('|', 'F', '7') is an odd num -> in loop
# 'S' should be included above if it is an 'upward wall' or 'downward wall'
def in_loop(grid: list, pos: tuple, upward_walls: list) -> bool:
	count = 0
	for row in range(len(grid)):
		if row == pos[0]:
			for col in range(len(grid[row])):
				if col < pos[1]:
					if is_pipe((row, col), pipe) and grid[row][col] in upward_walls:
						count += 1
			return count % 2 != 0

if get_s_value(pipe) in ['|', 'L', 'J']:
	upward_walls = ['|', 'L', 'J', 'S']
else:
	upward_walls = ['|', 'L', 'J']

count = 0
for row in range(len(grid)):
	for col in range(len(grid[row])):
		if not is_pipe((row, col), pipe):
			if in_loop(grid, (row, col), upward_walls):
				count += 1

print(f"part2: {count}")
