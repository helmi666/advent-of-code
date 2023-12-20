from collections import deque

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

if __name__ == "__main__":
	with open("input/day20.txt") as file:
		data = file.read().splitlines()

	flip_flops = []
	conjunctions = []
	for line in data:
		sender, recipients_str = line.split(' -> ')
		name = sender[1:]
		recipients = recipients_str.split(", ")
		if sender[0] == '%':
			flip_flops.append(FlipFlop(name, recipients))
		elif sender[0] == '&':
			conjunctions.append(Conjunction(name, recipients))
		else:
			broadcaster = Broadcaster(recipients)
	for line in data:
		sender, recipients = line.split(' -> ')
		for c in conjunctions:
			if c.name in recipients:
				name = sender
				if '%' in sender or '&' in sender:
					name = sender[1:]
				c.add_input_modules(name)

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
	print("part1:", count_high * count_low)
