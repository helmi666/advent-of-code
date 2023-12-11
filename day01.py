# part one
def get_first_num(line: str) -> int:
	for char in line:
		try:
			return int(char)
		except:
			continue

def get_last_num(line: str) -> int:
	i = len(line) - 1
	while i >= 0:
		try:
			return int(line[i])
		except:
			i -= 1

nums = []
with open("input/day1.txt") as file:
	for line in file:
		nums.append(get_first_num(line)*10 + get_last_num(line))

print(sum(nums))

# part two
digits = {"one": '1', "two": '2', "three": '3', "four": '4', "five": '5', 
			"six": '6', "seven": '7', "eight": '8', "nine": '9', 
			'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
			'7': '7', '8': '8', '9': '9'}

def parse_line(line: str) -> list:
	nums = []
	for word in digits:
		if word in line:
			indices = [index for index in range(len(line)) if line.find(word, index) == index]
			if indices != []:
				for index in indices:
					nums.append((index, digits[word]))
	return nums

results = []
with open("day1.txt") as file:
	for line in file:
		nums = parse_line(line)
		sorted_list = sorted(nums, key=lambda x: x[0])
		result = 10*(int(sorted_list[0][-1])) + int(sorted_list[-1][-1])
		results.append(result)

print(sum(results))
