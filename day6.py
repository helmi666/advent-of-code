# helper func: count the possibilities one can win
def count_winning(time: int, ref_dist: int) -> int:
	winning_dists = []
	# charge time is always between 0 and total_time
	for charge_time in range(time + 1):
		dist = charge_time * (time - charge_time)
		if dist > ref_dist:
			winning_dists.append(dist)
	return len(winning_dists)

""" part one """
# save the data to a dict: key = time, value = distance
with open("day6.txt") as file:
	data = file.readlines()

for i in range(2):
	data[i] = data[i].rstrip().split(':')[1].split()
	data[i] = [int(item) for item in data[i]]

time_dist = {}
for i in range(4):
	time_dist[data[0][i]] = data[1][i]

result = 1
for time, dist in time_dist.items():
	result *= count_winning(time, dist)

print(result)

""" part two """
with open("day6.txt") as file:
	new_data = file.readlines()

time = 0
for char in new_data[0]:
	if char.isdigit():
		time = 10 * time + int(char)

ref_dist = 0
for char in new_data[1]:
	if char.isdigit():
		ref_dist = 10 * ref_dist + int(char)

print(count_winning(time, ref_dist))
