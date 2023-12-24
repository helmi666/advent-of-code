import numpy as np
from itertools import combinations
from z3 import Int, Solver, sat

class Hailstone:
	# position (px, py, pz) and velocity (vx, vy, vz)
	def __init__(self, px: int, py: int, pz: int, vx: int, vy: int, vz: int):
		self.px = px
		self.py = py
		self.pz = pz
		self.vx = vx
		self.vy = vy
		self.vz = vz
	
	# will the paths of self and another intersect within a given area (not collide)
	def will_intersect(self, another: "Hailstone", limits: tuple) -> bool:
		lower = limits[0]
		upper = limits[1]

		m1 = self.vy / self.vx
		m2 = another.vy / another.vx

		# if having same slope in their velocity vectors -> 
		# two hailstones moving at the same direction -> will not intersect
		if m1 == m2:
			return False

		def get_y_intercept(px: int, py: int, vx: int, vy: int) -> int:
			point_vector = np.array([px, py])
			velocity_vector = np.array([vx, vy])

			# parametric equations of the line
			def x(t):
				return point_vector[0] + t * velocity_vector[0]

			def y(t):
				return point_vector[1] + t * velocity_vector[1]

			# when x equals to 0
			t_intercept = -point_vector[0] / velocity_vector[0]
			y_intercept = y(t_intercept)

			return y_intercept

		# line equation: y = ax + b (a: slope, b: y-intercept)
		# y1, y2 -> y-intercepts of the lines
		# m1 * x + y1 = m2 * x + y2 (same y for both lines -> lines intersect)
		y1 = get_y_intercept(self.px, self.py, self.vx, self.vy)
		y2 = get_y_intercept(another.px, another.py, another.vx, another.vy)
		x = (y2 - y1) / (m1 - m2)
		y = m1 * x + y1

		# if intersection is outside the area
		if not (lower <= x <= upper and lower <= y <= upper):
			return False

		t1 = (x - self.px) / self.vx
		t2 = (x - another.px) / another.vx
		# if intersection is in the future
		if t1 >= 0 and t2 >= 0:
			return True
		# if intersection is in the past
		else:
			return False

if __name__ == "__main__":
	with open("input/day24.txt") as file:
		data = file.read().splitlines()
	
	data = [line.split(" @ ") for line in data]
	data = [[parameter.split(", ") for parameter in hailstone] for hailstone in data]
	data = [[[int(num) for num in parameter] for parameter in hailstone] for hailstone in data]
	
	hailstones = []
	for hailstone in data:
		px, py, pz = hailstone[0]
		vx, vy, vz = hailstone[1]
		hailstones.append(Hailstone(px, py, pz, vx, vy, vz))

	# part one
	# x, y position each at least limits[0] and at most limits[1]
	limits = (200000000000000, 400000000000000)

	count = 0
	for pair in combinations(hailstones, 2):
		hailstone1, hailstone2 = pair
		if hailstone1.will_intersect(hailstone2, limits):
			count += 1
	print("part1:", count)

	# part two
	x = Int('x')
	y = Int('y')
	z = Int('z')
	vx = Int('vx')
	vy = Int('vy')
	vz = Int('vz')
	solver = Solver()
	for i, hailstone in enumerate(hailstones):
		x_i, y_i, z_i = hailstone.px, hailstone.py, hailstone.pz
		vx_i, vy_i, vz_i = hailstone.vx, hailstone.vy, hailstone.vz
		t_i = Int(f"t_{i}")
		solver.add(x_i + vx_i * t_i == x + vx * t_i)
		solver.add(y_i + vy_i * t_i == y + vy * t_i)
		solver.add(z_i + vz_i * t_i == z + vz * t_i)

	if solver.check() == sat:
		model = solver.model()
		print("part2:", model[x].as_long() + model[y].as_long() + model[z].as_long())
	else:
		print("no solution found")
