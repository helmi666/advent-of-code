# get data from the file
with open("day3.txt") as file:
	line_list = file.readlines()

all_nums = {}
for row in range(len(line_list)):
	current_number = ""
	num_start = False
	for col in range(len(line_list[row])):
		if line_list[row][col].isdigit():
			current_number += line_list[row][col]
			if not num_start:
				num_start_col = col
			num_start = True
		elif current_number:
			if int(current_number) not in all_nums:
				all_nums[int(current_number)] = [(row, num_start_col, col - 1)]
			else:
				all_nums[int(current_number)].append((row, num_start_col, col - 1))
			current_number = ""
			num_start = False

# part one
def is_symbol(char: str) -> bool:
	if char.isdigit():
		return False
	if char == '.':
		return False
	if char == '\n':
		return False
	return True

def cordinates_valid(current_crds: tuple) -> bool:
	for row in range(len(line_list)):
		if row == current_crds[0] - 1:
			for col in range(len(line_list[row])):
				if current_crds[1] - 1 <= col <= current_crds[2] + 1:
					if is_symbol(line_list[row][col]):
						return True
		if row == current_crds[0]:
			for col in range(len(line_list[row])):
				if current_crds[1] - 1 == col or col == current_crds[2] + 1:
					if is_symbol(line_list[row][col]):
						return True
		if row == current_crds[0] + 1:
			for col in range(len(line_list[row])):
				if current_crds[1] - 1 <= col <= current_crds[2] + 1:
					if is_symbol(line_list[row][col]):
						return True
	return False

result = 0
for num, cordinates in all_nums.items():
	valid_coordinates = []
	for current_crds in cordinates:
		if cordinates_valid(current_crds):
			valid_coordinates.append(current_crds)
	result += num * len(valid_coordinates)

print(result)

# part two
def find_adjacent_nums(all_nums: dict, row: int, col: int, gears: dict):
	for num, coordinates in all_nums.items():
		for current_crd in coordinates:
			if row - 1 <= current_crd[0] <= row + 1:
				if (col -1 <= current_crd[1] <= col + 1) or (col -1 <= current_crd[2] <= col + 1):
					gears[(row, col)].append((num, current_crd))

gears = {}
for row in range(len(line_list)):
	for col in range(len(line_list[row])):
		if line_list[row][col] == '*':
			gears[(row, col)] = []
			find_adjacent_nums(all_nums, row, col, gears)
			
result = 0
for gear, digits in gears.items():
	if len(digits) == 2:
		result += digits[0][0] * digits[1][0]
print(result)
