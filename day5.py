""" helper funcs and get data from the file """
def parse_maps(data: list, start_line: str, end_line: str) -> dict:
	start_index = data.index(start_line)
	if end_line != "eof":
		end_index = data.index(end_line)
	else:
		end_index = len(data)
	extracted = data[start_index + 1 : end_index]
	extracted = [line.split() for line in extracted]
	extracted = [[int(num) for num in sublist] for sublist in extracted]
	return extracted

with open("day5.txt") as file:
	data = file.readlines()

data = [line.rstrip() for line in data]
data = [line for line in data if line != '']

# get seeds numbers
seeds = data[0].split(':')[1].split()
seeds = [int(item) for item in seeds]

# parse info in each map into list
seed_to_soil = parse_maps(data, "seed-to-soil map:", "soil-to-fertilizer map:")
soil_to_fert = parse_maps(data, "soil-to-fertilizer map:", "fertilizer-to-water map:")
fert_to_water = parse_maps(data, "fertilizer-to-water map:", "water-to-light map:")
water_to_light = parse_maps(data, "water-to-light map:", "light-to-temperature map:")
light_to_tem = parse_maps(data, "light-to-temperature map:", "temperature-to-humidity map:")
tem_to_hum = parse_maps(data, "temperature-to-humidity map:", "humidity-to-location map:")
hum_loc = parse_maps(data, "humidity-to-location map:", "eof")
maps = [seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_tem, tem_to_hum, hum_loc]

""" part one """
def find_loc(maps: list, seed: int) -> int:
	temp = seed
	for map in maps:
		for line in map:
			if line[1] <= temp < line[1] + line[2]:
				temp = temp + (line[0] - line[1])
				break
	return temp

# get locations for corresponding seeds
locs = []
for seed in seeds:
	loc = find_loc(maps, seed)
	locs.append(loc)
print(min(locs))

""" part two """
# reversed search (from location to seed)
maps.reverse()
def find_seed(maps: list, loc: int) -> int:
	temp = loc
	for map in maps:
		for line in map:
			if line[0] <= temp < line[0] + line[2]:
				temp = temp - (line[0] - line[1])
				break
	return temp

def is_even(number):
    return number % 2 == 0

# check if the given seed is in the ranges
def seed_exist(seed_num: int, avail_seeds: list) -> bool:
	seeds_range = []
	for i in range(len(avail_seeds)):
		if is_even(i):
			seeds_range.append((avail_seeds[i], avail_seeds[i] + avail_seeds[i + 1]))
	for current_range in seeds_range:
		if current_range[0] <= seed_num < current_range[1]:
			return True
	return False

# imcrement location from 0 until existing seed is found
for loc in range(2147483647):
	seed_num = find_seed(maps, loc)
	if seed_exist(seed_num, seeds):
		print(seed_num)
		print(loc)
		break
