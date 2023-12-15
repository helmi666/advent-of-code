def hash_func(string) -> int:
	res = 0
	for char in string:
		ascii_value = ord(char)
		res += ascii_value
		res *= 17
		res %= 256
	return res

if __name__ == "__main__":
	with open("input/day15.txt") as file:
		data = file.read().split(',')

	# part one
	res = 0
	for step in data:
		res += hash_func(step)

	print("part1:", res)

	# part two
	boxes = {}
	for step in data:
		label = ''.join(char for char in step if char.isalpha())
		box_num = hash_func(label)
		if box_num not in boxes:
			boxes[box_num] = []
		if '=' in step:
			focal_len = int(step.split('=')[1])
			if label not in [lens[0] for lens in boxes[box_num]]:
				boxes[box_num].append([label, focal_len])
			else:
				for lens in boxes[box_num]:
					if lens[0] == label:
						lens[1] = focal_len
		if '-' in step:
			for box, lenses in boxes.items():
				for lens in lenses:
					if lens[0] == label:
						lenses.remove(lens)

	res = 0
	for box_num, lenses in boxes.items():
		for index, lens in enumerate(lenses):
			res += (box_num + 1) * (index + 1) * lens[1]
	
	print("part2", res)
