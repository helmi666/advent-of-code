# part one
def check_cube(cube_set: str) -> bool:
	cube_subset = cube_set.split(',')
	# check if num of red cubes exceed 12
	for item in cube_subset:
		if "red" in item:
			num = int(item.split(' ')[1])
			if num > 12:
				return False
		if "green" in item:
			num = int(item.split(' ')[1])
			if num > 13:
				return False
		if "blue" in item:
			num = int(item.split(' ')[1])
			if num > 14:
				return False
	return True

results = []
with open("input/day2.txt") as file:
	for line in file:
		cube_sets = line.rstrip().split(';')
		# get game num
		game_num = int(cube_sets[0].split(':')[0].split(' ')[1])
		cube_sets[0] = cube_sets[0].split(':')[1]
		is_possible = True
		for cube_set in cube_sets:
			if not check_cube(cube_set):
				is_possible = False
				break
		if is_possible:
			results.append(game_num)

print(sum(results))

# part two
def get_nums(cube_set: str) -> list:
	cube_subset = cube_set.split(',')
	red_num = 0
	green_num = 0
	blue_num = 0
	# check if num of red cubes exceed 12
	for item in cube_subset:
		if "red" in item:
			red_num = int(item.split(' ')[1])
		if "green" in item:
			green_num = int(item.split(' ')[1])
		if "blue" in item:
			blue_num = int(item.split(' ')[1])
	return [red_num, green_num, blue_num]

results = []
with open("day2.txt") as file:
	for line in file:
		cube_sets = line.rstrip().split(';')
		# get game num
		game_num = int(cube_sets[0].split(':')[0].split(' ')[1])
		cube_sets[0] = cube_sets[0].split(':')[1]
		is_possible = True
		nums = [0, 0, 0]
		for cube_set in cube_sets:
			temp_list = get_nums(cube_set)
			for i in range(3):
				if temp_list[i] > nums[i]:
					nums[i] = temp_list[i]
		result = nums[0]*nums[1]*nums[2]
		results.append(result)

print(sum(results))
