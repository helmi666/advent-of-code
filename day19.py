from copy import deepcopy

def sort(parts: dict, workflows: dict) -> str:
	x = parts['x']
	m = parts['m']
	a = parts['a']
	s = parts['s']
	act = "in"
	while True:
		for exp in workflows[act][:-1]:
			cond = exp.split(':')[0]
			if all(char.isdigit() or char in "xmas><" for char in cond):
				cond_fulfilled = eval(cond)
			else:
				print("invalid expression")
			if cond_fulfilled:
				act = exp.split(':')[1]
				break
		else:
			act = workflows[act][-1]
		if act == 'A' or act == 'R':
			break
	return act

def count(rng: dict) -> int:
	res = 1
	for r in rng.values():
		res = res * (r[1] - r[0] + 1)
	return res 

def run(rng: dict, workflows: dict, workflow: str) -> int:
	res = 0
	for exp in workflows[workflow]:
		if ':' in exp:
			cond, act = exp.split(':')
			if '>' in cond:
				cat, value = cond.split('>')
				new_rng = deepcopy(rng)
				if new_rng[cat][1] > int(value):
					new_rng[cat][0] = max(new_rng[cat][0], int(value) + 1)
					if act == 'A':
						res += count(new_rng)
					elif act != 'R':
						res += run(new_rng, workflows, act)
					rng[cat][1] = int(value)
			elif '<' in cond:
				cat, value = cond.split('<')
				new_rng = deepcopy(rng)
				if new_rng[cat][0] < int(value):
					new_rng[cat][1] = min(new_rng[cat][1], int(value) - 1)
					if act == 'A':
						res += count(new_rng)
					elif act != 'R':
						res += run(new_rng, workflows, act)
					rng[cat][0] = int(value)
		else:
			if exp == 'A':
				res += count(rng)
			elif exp != 'R':
				res += run(rng, workflows, exp)
	return res

if __name__ == "__main__":
	with open("input/day19.txt") as file:
		data = file.read().splitlines()

	nl_index = data.index("")
	workflows_data = data[:nl_index]
	ratings = data[nl_index + 1:]

	workflows = {}
	for line in workflows_data:
		key_value_pairs = line[:-1].split('{')
		key = key_value_pairs[0]
		value = key_value_pairs[1]
		workflows[key] = value.split(',')

	# part one
	parts_lst = []
	for line in ratings:
		key_value_pairs = line[1:-1].split(',')
		parts = {}
		for pair in key_value_pairs:
			key, value = pair.split('=')
			parts[key] = int(value)
		parts_lst.append(parts)

	total = 0
	for parts in parts_lst:
		status = sort(parts, workflows)
		if status == 'A':
			total += sum(parts.values())
	print("part1:", total)
	
	# part two
	rng = {
		'x': [1, 4000],
		'm': [1, 4000],
		'a': [1, 4000],
		's': [1, 4000]
	}

	total = run(rng, workflows, "in")
	print("part2:", total)
