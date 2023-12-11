import math

# parse instructions into string, network into dict
with open("day8.txt") as file:
	data = file.readlines()

instr = data[0].rstrip()

nodes = {}
for line in data[2:]:
	lst = line.split()
	lst = [''.join(filter(str.isalpha, s)) for s in lst]
	nodes[lst[0]] = (lst[2], lst[3])

""" part one """
steps = 0
# initially, next location (the location to search for in dict) is set to "AAA"
next_loc = "AAA"
while True:
	for dirct in instr:
		for loc, dest in nodes.items():
			if next_loc == "ZZZ":
				break
			if loc == next_loc:
				steps += 1
				if dirct == 'L':
					next_loc = dest[0]
				else:
					next_loc = dest[1]
				break
		if next_loc == "ZZZ":
			break
	if next_loc == "ZZZ":
			break
print(f"part1: {steps}")

""" part two """
def last_char(string: str) -> str:
	return string[-1]

# search for all nodes starting with "**A" and save to a list
start_locs = []
for loc in nodes:
	if last_char(loc) == 'A':
		start_locs.append(loc)

# record minimum steps required for each route ("**A" -> ... -> "**Z")
steps_lst = []
for start_loc in start_locs:
	steps = 0
	next_loc = start_loc
	while True:
		for dirct in instr:
			for loc, dest in nodes.items():
				if last_char(next_loc) == 'Z':
					break
				if loc == next_loc:
					steps += 1
					if dirct == 'L':
						next_loc = dest[0]
					else:
						next_loc = dest[1]
					break
			if last_char(next_loc) == 'Z':
				break
		if last_char(next_loc) == 'Z':
				break
	steps_lst.append(steps)

# verify if all the steps are divisible by len(instr), 
# i.e. if all routes take full circles of instructions to finish
lcm_usable = True
for num in steps_lst:
	if num % len(instr) != 0:
		lcm_usable = False
print(f"lcm_usable: {lcm_usable}")

print(f"part2: {math.lcm(*steps_lst)}")
