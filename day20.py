from collections import deque
from math import lcm
from copy import deepcopy

class FlipFlop:
	# off -> False, on -> True
	# initialized to false(off)
	def __init__(self, name: str, recipients: list, status: str=False):
		self.name = name
		self.status = status
		self.recipients = recipients
		self.count_low = 0
		self.count_high = 0
	
	def output(self, pulse: str) -> str:
		if pulse == "low":
			self.status = not self.status
		if self.status:
			self.count_high += len(self.recipients)
			return "high"
		else:
			self.count_low += len(self.recipients)
			return "low"

class Conjunction:
	def __init__(self, name: str, recipients: list):
		self.name = name
		self.recipients = recipients
		self.pulses = {}
		self.count_low = 0
		self.count_high = 0

	# initialized to remembering a low pulse for each input
	def add_input_modules(self, module: str):
		self.pulses[module] = "low"
	
	def output(self, module: str, pulse: str) -> str:
		self.pulses[module] = pulse
		if all(value == "high" for value in self.pulses.values()):
			self.count_low += len(self.recipients)
			return "low"
		else:
			self.count_high += len(self.recipients)
			return "high"

class Broadcaster:
	def __init__(self, recipients: list, name: str="broadcaster"):
		self.name = name
		self.recipients = recipients
		self.count_low = 0
		self.count_high = 0

	def output(self, pulse: str) -> str:
		if pulse == "low":
			self.count_low += len(self.recipients)
		else:
			self.count_high += len(self.recipients)
		return pulse

def copy_data() -> tuple:
	broadcaster = deepcopy(broadcaster_orig)
	flip_flops = deepcopy(flip_flops_orig)
	conjunctions = deepcopy(conjunctions_orig)
	return broadcaster, flip_flops, conjunctions

if __name__ == "__main__":
	with open("input/day20.txt") as file:
		data = file.read().splitlines()

	flip_flops_orig = []
	conjunctions_orig = []
	for line in data:
		sender, recipients_str = line.split(' -> ')
		name = sender[1:]
		recipients = recipients_str.split(", ")
		if sender[0] == '%':
			flip_flops_orig.append(FlipFlop(name, recipients))
		elif sender[0] == '&':
			conjunctions_orig.append(Conjunction(name, recipients))
		else:
			broadcaster_orig = Broadcaster(recipients)
	for line in data:
		sender, recipients = line.split(' -> ')
		for c in conjunctions_orig:
			if c.name in recipients:
				name = sender
				if '%' in sender or '&' in sender:
					name = sender[1:]
				c.add_input_modules(name)

	# part one
	broadcaster, flip_flops, conjunctions = copy_data()
	for i in range(1000):
		queue = deque()
		pulse = broadcaster.output("low")
		for recipient in broadcaster.recipients:
			queue.append((broadcaster.name, pulse, recipient))
		while queue:
			sender, pulse, recipient = queue.popleft()
			for ff in flip_flops:
				if ff.name == recipient:
					if pulse == "high":
						break
					pulse_next = ff.output(pulse)
					for r in ff.recipients:
						queue.append((ff.name, pulse_next, r))
					break
			for cj in conjunctions:
				if cj.name == recipient:
					pulse_next = cj.output(sender, pulse)
					for r in cj.recipients:
						queue.append((cj.name, pulse_next, r))
					break
			if all(f.status == False for f in flip_flops):
				if all(value == "low" for cj in conjunctions for value in cj.pulses.values()):
					break
	
	count_low = broadcaster.count_low + 1000
	count_high = broadcaster.count_high
	for ff in flip_flops:
		count_low += ff.count_low
		count_high += ff.count_high
	for cj in conjunctions:
		count_low += cj.count_low
		count_high += cj.count_high

	print("part1:", count_low * count_high)
	
	# part two (hard coded, after studying the pattern of input)
	# only when four modules (xn, qn, xf, zl) all send high pulse to th module
	# th will then sends low pulse to rx
	xn_high_found = False
	qn_high_found = False
	xf_high_found = False
	zl_high_found = False
	solution_found = False
	rounds = []
	broadcaster, flip_flops, conjunctions = copy_data()

	for i in range(100000):
		queue = deque()
		pulse = broadcaster.output("low")
		for recipient in broadcaster.recipients:
			queue.append((broadcaster.name, pulse, recipient))
		while queue:
			sender, pulse, recipient = queue.popleft()
			for ff in flip_flops:
				if ff.name == recipient:
					if pulse == "high":
						break
					pulse_next = ff.output(pulse)
					for r in ff.recipients:
						queue.append((ff.name, pulse_next, r))
					break
			for cj in conjunctions:
				if cj.name == recipient:
					pulse_next = cj.output(sender, pulse)
					for r in cj.recipients:
						queue.append((cj.name, pulse_next, r))
					break
			if ('xn', 'high', 'th') in queue and not xn_high_found:
				rounds.append(i + 1)
				xn_high_found = True
			if ('qn', 'high', 'th') in queue and not qn_high_found:
				rounds.append(i + 1)
				qn_high_found = True
			if ('xf', 'high', 'th') in queue and not xf_high_found:
				rounds.append(i + 1)
				xf_high_found = True
			if ('zl', 'high', 'th') in queue and not zl_high_found:
				rounds.append(i + 1)
				zl_high_found = True
			if xn_high_found and qn_high_found and xf_high_found and zl_high_found:
				solution_found = True
				break
			if all(f.status == False for f in flip_flops):
				if all(value == "low" for cj in conjunctions for value in cj.pulses.values()):
					break
		if solution_found:
			break
	
	print("part2:", lcm(*rounds))
