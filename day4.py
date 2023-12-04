# helper funcs
def	get_winning_nums(line: str) -> list:
	line = line.split('|')[0].split(':')[1]
	items = line.split(' ')
	nums = [num for num in items if num != '']
	return nums

def get_my_nums(line: str) -> list:
	line = line.split('|')[1].rstrip()
	items = line.split(' ')
	nums = [num for num in items if num != '']
	return nums

def count_matches(line: str) -> int:
	winning_nums = get_winning_nums(line)
	my_nums = get_my_nums(line)
	count = 0
	for num in my_nums:
		if num in winning_nums:
			count += 1
	return count

with open("day4.txt") as file:
	line_list = file.readlines()

# part one
points = 0
for line in line_list:
	count = count_matches(line)
	if count >= 1:
		points += 2 ** (count - 1)

print(points)

# part two
original_cards = len(line_list)
# create a dict: key = card id, value = num of cards (original + copies)
cards = {}
for i in range(original_cards):
	cards[i] = 1

for line_id in range(original_cards):
	line = line_list[line_id]
	count = count_matches(line)
	for j in range(cards[line_id]):
		for k in range(count):
			cards[line_id + k + 1] += 1

total_cards = 0
for card_id, num_cards in cards.items():
	total_cards += num_cards

print(total_cards)
