import settings
import random

class Encoding():
	"""
	Represents the encoding of an individual.
	Subclasses implement actual mutate and recombine method
	"""
	def mutate(self):
		raise NotImplemented # TODO verificare il nome di questa eccezione

	def recombine(self, other):
		raise NotImplemented # TODO verificare il nome di questa eccezione

	def __str__(self):
		raise NotImplemented # TODO verificare il nome di questa eccezione
	
	def __len__(self):
		raise NotImplemented # TODO verificare il nome di questa eccezione

class Fitness():
	def __float__(self):
		raise NotImplemented # TODO verificare il nome di questa eccezione
	
	def __add__(self, other):
		"""
		Sums fitness, return a float (not a fitness)
		"""
		return float(self) + float(other)

	def __radd__(self, other):
		"""
		Sums fitness, return a float (not a fitness)
		"""
		return float(self) + float(other)
	
	def win(self, over = None):
		raise NotImplemented # TODO verificare il nome di questa eccezione

	def lose(self, by = None):
		raise NotImplemented # TODO verificare il nome di questa eccezione


class AlphabeticEncoding(Encoding):
	def __init__(self, sequence = None):
		if sequence != None:
			self.sequence = sequence
		else:
			self.sequence = ''
			length = random.randint(1, settings.MAX_ALPHABETIC_INDIVIDUAL_INIT_LENGTH)
			for i in range(length):
				self.sequence += random.choice(settings.ALPHABET)

	def __str__(self):
		return '"%s"' % self.sequence

	def __len__(self):
		return len(self.sequence)

	# metodi di mutazione
	def mutate_single_char(self, char = None):
		"""
		substitute a single position with char
		if char is submitted a random char is chosen
		"""
		i = random.randrange(len(self.sequence))
		if char == None: char = random.choice(settings.ALPHABET)
		self.sequence = self.sequence[:i] + char + self.sequence[i+1:]

	def mutate_chars_with_probability(self, prob):
		"""
		sustitute each position with a random char with probability "prob"
		"""
		new_sequence = ""
		for char in self.sequence:
			if chance(probe):
				new_sequence += random.choice(settings.ALPHABET)
			else:
				new_sequence += char
		self.sequence = new_sequence

	def mutate_invert(self):
		"""
		invert the string
		"""
		self.sequence = reduce(lambda x,y: y + x, self.sequence)

	def mutate_switch(self):
		"""
		pick a random position x and returns sequence[x:] + sequence[:x]
		"""
		i = random.randrange(len(self.sequence))
		self.sequence = self.sequence[i:] + self.sequence[:i]

	def mutate_skip(self):
		"""
		remove a random substring from the string
		"""
		self.mutate_single_char(char = "")

	# metodi di ricombinazione
	def single_point_crossover(self, other):
		i = random.randrange(len(self.sequence))
		j = random.randrange(len(other.sequence))
		return (Encoding(self.sequence[:i] + other.sequence[j:]),
				Encoding(other.sequence[:j] + self.sequence[i:]))

class WonPlayedFitness(Fitness):
	def __init__(self):
		self.won = 0
		self.played = 0
	
	def __float__(self):
		return (self.won / self.played) + 1 if self.played != 0 else 0

# Funzione ausiliarie
def chance(probability = 0.5):
	"""
	Returns true probability*100 times out of 100 calls
	"""
	return random.random() < probability
