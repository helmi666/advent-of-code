def get_pattern(data: list) -> list:
	if '\n' in data:
		separator_index = data.index('\n')
		pattern = data[:separator_index]
		data[:] = data[separator_index + 1:]
	else:
		pattern = data[:]
		data[:] = []
	pattern = [line.rstrip() for line in pattern]
	pattern = [list(row) for row in pattern]
	return pattern

# optional paramater old_res is for part two - to get a new result
# in case old result is also horizontal
def check_h_mirror(pattern: list, old_res: int=None) -> int:
	is_valid = False
	# if mirror is between rows indexed i and i + 1 
	for i in range(0, len(pattern) - 1):
		if old_res != None:
			if i != old_res - 1:
				# check if assumption is valid
				for j in range(0, min(i + 1, len(pattern) - i - 1)):
					if pattern[i - j] != pattern[i + 1 + j]:
						is_valid = False
						break
					is_valid = True
				if is_valid:
					# return index + 1, as row num starts from 1
					return i + 1
		else:
			for j in range(0, min(i + 1, len(pattern) - i - 1)):
				if pattern[i - j] != pattern[i + 1 + j]:
					is_valid = False
					break
				is_valid = True
			if is_valid:
				return i + 1
	# return -1 to indicate no mirror is found
	return -1

def check_v_mirror(pattern: list, old_res: int=None) -> int:
	is_valid = False
	for i in range(0, len(pattern[0]) - 1):
		if old_res != None:
			if i != old_res - 1:
				for j in range(0, min(i + 1, len(pattern[0]) - i - 1)):
					if [row[i - j] for row in pattern] != [row[i + 1 + j] for row in pattern]:
						is_valid = False
						break
					is_valid = True
				if is_valid:
					return i + 1
		else:
			for j in range(0, min(i + 1, len(pattern[0]) - i - 1)):
				if [row[i - j] for row in pattern] != [row[i + 1 + j] for row in pattern]:
					is_valid = False
					break
				is_valid = True
			if is_valid:
				return i + 1
	return -1

def reverse_ash_rock(pattern: list, row: int, col: int):
	char = pattern[row][col]
	if char == '#':
		pattern[row][col] = '.'
	else:
		pattern[row][col] = '#'

if __name__ == "__main__":
	with open("input/day13.txt") as file:
		data = file.readlines()

	data_cpy = data[:]
	counter_part1 = 0
	counter_part2 = 0
	while data_cpy != []:
		# process one parttern as a time
		pattern = get_pattern(data_cpy)
		# get old results (part 1 + part 2)
		h_mirror_found = check_h_mirror(pattern)
		if h_mirror_found != -1:
			old_res = h_mirror_found
			counter_part1 += old_res * 100
		else:
			old_res = check_v_mirror(pattern)
			counter_part1 += old_res
		# get new results (part 2)
		new_res_found = False
		for row in range(len(pattern)):
			for col in range(len(pattern[row])):
				reverse_ash_rock(pattern, row, col)
				# if the change leads to a NEW solution
				if h_mirror_found != -1:
					res_row = check_h_mirror(pattern, old_res)
					if res_row != -1:
						new_res = res_row * 100
						new_res_found = True
						break 
					res_col = check_v_mirror(pattern)
					if res_col != -1:
						new_res = res_col
						new_res_found = True
						break
				else:
					res_row = check_h_mirror(pattern)
					if res_row != -1:
						new_res = res_row * 100
						new_res_found = True
						break 
					res_col = check_v_mirror(pattern, old_res)
					if res_col != -1:
						new_res = res_col
						new_res_found = True
						break
				# new solution not found, undo the change, and move to next cell
				reverse_ash_rock(pattern, row, col)
			if new_res_found:
				break
		counter_part2 += new_res
	print("part1", counter_part1)
	print("part2:", counter_part2)
