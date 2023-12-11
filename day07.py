# read data from file to a list of tuples
hands = []
with open("input/day7.txt") as file:
	for line in file:
		line = line.split()
		hands.append((line[0], int(line[1])))

# count num of 'J' in hand
def count_j(hand: str) -> int:
	return hand.count('J')

# count max num of same chars
def count_max_chars(hand: str, joker_rule: bool):
	if joker_rule:
		counts = []
		for item in set(hand):
			if item != 'J':
				counts.append(hand.count(item))
		return max(counts) + count_j(hand)
	else:
		counts = []
		for item in set(hand):
			counts.append(hand.count(item))
		return max(counts)

# first rule to consider when sorting hands
def first_rule(hand: str, joker_rule: bool) -> int:
	# count num of unique elements in hands
	set_count = len(set(hand))
	if joker_rule:
		modify_set_count = 0
		if count_j(hand) != 0:
			modify_set_count = -1
		if len(set(hand)) != 1:
			set_count += modify_set_count
	if set_count == 5:
		return 1
	if set_count == 4:
		return 2
	if set_count == 3:
		if count_max_chars(hand, joker_rule) == 2:
			return 3
		elif count_max_chars(hand, joker_rule) == 3:
			return 4
	if set_count == 2:
		if count_max_chars(hand, joker_rule) == 3:
			return 5
		elif count_max_chars(hand, joker_rule) == 4:
			return 6
	if set_count == 1:
		return 7

# second rule to consider when sorting hands
def second_rule(hand: str, ref_str) -> list:
	index_list = []
	for char in hand:
		index_list.append(ref_str.find(char))
	return index_list

# sorting rules for part one
def sorting_rules_part1(hand: str) -> tuple:
	return first_rule(hand[0], 0), second_rule(hand[0], "23456789TJQKA")

# sorting rules for part two
def sorting_rules_part2(hand: str) -> tuple:
	return first_rule(hand[0], 1), second_rule(hand[0], "J23456789TQKA")

sorted_list_part1 = sorted(hands, key=sorting_rules_part1)
sorted_list_part2 = sorted(hands, key=sorting_rules_part2)

def	get_result(sorted_list: list) -> int:
	result = 0
	for i in range(len(sorted_list)):
		result += sorted_list[i][1] * (i + 1)
	return result

print(f"Part1 result: {get_result(sorted_list_part1)}")
print(f"Part2 result: {get_result(sorted_list_part2)}")
