# parse data from file into a list of sublists(histories)
with open("day9.txt") as file:
	data = file.readlines()

data = [item.rstrip().split() for item in data]

data = [[int(num) for num in history] for history in data]

def all_zeros(lst: list) -> bool:
	if lst == []:
		return False
	for item in lst:
		if item != 0:
			return False
	return True

""" part one """
# find next value based on history using recursion
def next_value(history: list) -> int:
	if not all_zeros(history):
		new_lst = []
		for i in range(len(history) - 1):
			diff = history[i + 1] - history[i]
			new_lst.append(diff)
		last_diff = next_value(new_lst)
		return last_diff + history[-1]
	else:
		return 0

next_values = [next_value(history) for history in data]

print(f"part1: {sum(next_values)}")

""" part two """
# same approach used for finding prev value
def prev_value(history: list) -> int:
	if not all_zeros(history):
		new_lst = []
		for i in range(len(history) - 1):
			diff = history[i + 1] - history[i]
			new_lst.append(diff)
		last_diff = prev_value(new_lst)
		return history[0] - last_diff
	else:
		return 0

prev_values = [prev_value(history) for history in data]

print(f"part2: {sum(prev_values)}")
