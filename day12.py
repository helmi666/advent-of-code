# count number of arrangements
# parameters i and j refer to index of spring in springs, and index of group in groups
def count_arrs(springs: str, groups: list, i: int, j: int) -> int:
	# ending conditions in the recursive func
	# if all springs are checked, but not all broken groups are checked -> not a solution
	if i >= len(springs) and j < len(groups):
		return 0
	if j >= len(groups):
		# if all broken groups are checked, but a broken spring is found in remaining springs -> not a solution
		if i < len(springs) and '#' in springs[i:]:
			return 0
		# else, one solution found (every time, when a solution is found, 1 will be added to counter)
		return 1
	
	# to improve efficiency, repetitive func calls can be avoided (esp. for deep recursions)
	# by saving results of decision makings (typical example: fibonacci sequence)
	# func calls goes up bottom whereas return value goes bottom up
	# next time when same decision making is needed, no further recursion will be repeated, 
	# instead, the result saved in cache is used.
	if (i, j) in MEMO:
		return MEMO[(i, j)]

	# group size for the group indexed j
	size = groups[j]

	# if spring is operational , go to next spring
	if springs[i] == '.':
		counter = count_arrs(springs, groups, i + 1, j)
	# if spring is broken, check if a broken group can be found starting from springs[i]
	elif springs[i] == '#':
		if '.' not in springs[i:i + size] and springs[i + size] != '#':
			# so far valid, continue verifying solution with remaining springs and groups
			counter = count_arrs(springs, groups, i + size + 1, j + 1)
		else:
			# not a valid solution
			return 0
	# if spring is unknown, it is either broken or operational
	elif springs[i] == '?':
		if '.' not in springs[i:i + size] and springs[i + size] != '#':
			# from springs[i], possible to start a group
			# search should be done with two possibilities (broken spring + operational spring)
			counter = count_arrs(springs, groups, i + size + 1, j + 1) + count_arrs(springs, groups, i + 1, j)
		else:
			# group cannot be formed -> spring is operational
			counter = count_arrs(springs, groups, i + 1, j)

	MEMO[(i, j)] = counter
	return counter

if __name__ == "__main__":
	with open("input/day12.txt") as file:
		data = file.readlines()
	
	# part one
	arrs_sum = 0
	for i in range(len(data)):
		line = data[i]
		line = line.rstrip()
		springs = line.split()[0]
		# one operational spring added as the validation condition of a group includes checking
		# if the spring immediately following the group is not a broken spring
		springs = springs + '.'

		groups = line.split()[1]
		groups = [int(size) for size in groups.split(',')]

		MEMO = {}
		arrs_sum += count_arrs(springs, groups, 0, 0)

	print(arrs_sum)

	# part two
	# memoization is mainly used for this part to store the results of expensive function calls 
	arrs_sum = 0
	for i in range(len(data)):
		line = data[i]
		line = line.rstrip()
		springs = line.split()[0]
		springs = '?'.join([springs] * 5)
		springs = springs + '.'

		groups = line.split()[1]
		groups = [int(size) for size in groups.split(',')] * 5

		MEMO = {}
		arrs_sum += count_arrs(springs, groups, 0, 0)

	print(arrs_sum)
