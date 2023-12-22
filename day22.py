from collections import deque

class Brick:
	# upon examming data, x1 <= x2, y1 <= y2, z1 <= z2
	def __init__(self, x1, y1, z1, x2, y2, z2):
		self.x1, self.y1, self.z1 = x1, y1, z1
		self.x2, self.y2, self.z2 = x2, y2, z2
		# bricks above to support
		self.parents = set()
		# bricks below supporting self
		self.children = set()
	
	def fall(self, settled: list):
		# if brick is on the ground
		if self.z1 == 1:
			return
		highest = 0
		supporting_bricks = []
		for brick in settled:
			# among bricks that overlap with self horizontally, the highest one(s) will support self
			if brick.x1 <= self.x1 <= brick.x2 or brick.x1 <= self.x2 <= brick.x2 or (self.x1 < brick.x1 and self.x2 > brick.x2):
				if brick.y1 <= self.y1 <= brick.y2 or brick.y1 <= self.y2 <= brick.y2 or (self.y1 < brick.y1 and self.y2 > brick.y2):
					if brick.z2 > highest:
						highest = brick.z2
						supporting_bricks = [brick]
					elif brick.z2 == highest:
						supporting_bricks.append(brick)
		if highest == 0:
			# no brick below supports self -> self falls to ground
			diff = self.z2 - self.z1
			self.z1 = 1
			self.z2 = 1 + diff
		else:
			# at least one brick can support self -> self falls to supporting brick(s)
			# dependencies get updated
			diff = self.z2 - self.z1
			self.z1 = highest + 1
			self.z2 = self.z1 + diff
			for brick in supporting_bricks:
				self.children.add(brick)
				brick.parents.add(self)

	def can_remove(self) -> bool:
		# if any of its parents depends on this brick -> cannot remove
		# depend -> has only one child
		for parent in self.parents:
			if len(parent.children) == 1:
				return False
		return True

	# how many bricks above would fall, if self is removed
	def cause_to_fall(self) -> int:
		queue = deque([self.parents])
		count = 0
		fallen = []
		while queue:
			parents = queue.popleft()
			for parent in parents:
				# if parent is already fallen, no need to check
				if parent in fallen:
					continue
				# if parent depends on self: self falls -> parent will fall
				if len(parent.children) == 1:
					count += 1
					fallen.append(parent)
					queue.append(parent.parents)
				# if parent depends on several children: all depending children fall -> parent will fall
				elif all(child in fallen for child in parent.children):
					count += 1
					fallen.append(parent)
					queue.append(parent.parents)
		return count

if __name__ == "__main__":
	with open("input/day22.txt") as file:
		data = file.read().split('\n')

	data = [line.split('~') for line in data]
	data = [[tuple([int(num) for num in coords.split(',')]) for coords in sublist] for sublist in data]
	data.sort(key=lambda x: x[0][2])

	bricks = []
	for line in data:
		x1, y1, z1 = line[0]
		x2, y2, z2 = line[1]
		brick = Brick(x1, y1, z1, x2, y2, z2)
		bricks.append(brick)

	# simulate falling process
	settled = []
	for brick in bricks:
		brick.fall(settled)
		settled.append(brick)
	bricks = settled		

	# part one
	count = 0
	for brick in bricks:
		if brick.can_remove():
			count += 1
	print("part1:", count)

	# part two
	count = 0
	for brick in bricks:
		count += brick.cause_to_fall()
	print("part2:", count)
