import random
import settings

class Individual(object):
	pass

class AlphabeticIndividual(Individual):
	def __init__(self, sequence = None):
		if sequence != None:
			self.sequence = sequence
		else:
			self.sequence = ''
			length = random.randint(1, settings.MAX_ALPHABETIC_INDIVIDUAL_INIT_LENGTH)
			for i in range(length):
				self.sequence += random.choose(settings.ALPHABET)
		self.played = 0
		self.won = 0
	

	def get_fitness(self):
		if self.played == 0:
			return 0
		return (sel.won / self.played)+1

	
	def __str__(self):
		return '"%s"' % self.sequence

	def __len__(self):
		"""
		Returns the length of the sequence.
		"""
		return len(self.sequence)



class Population(object):
	"""
	Genetic algorithm population management
	"""
	def __init__(self, size = settings.POPULATION_SIZE, individual_type=settings.INDIVIDUAL_TYPE):
		self.pool = []
		for i in range(size):
			self.pool.append(individual_type())

	def choose_random_individual(self, by_fitness = False):
		if by_fitness:
			# TODO usare una funzione esterna per scegliere
			pass
		else
			return random.choose(self.pool)

	def choose_random_couple(self, by_fitness = False):
		i1 = self.choose_random_individual(by_fitness = by_fitness)
		while True:
			i2 = self.choose_random_individual(by_fitness = by_fitness)
			if i1 not is i2: break
		return (i1, i2)

	def prune(self):
		# TODO Questo metodo dovrebbe essere esguito dopo ogni match
		# e potrebbe riordinare la popolazione in base alla fitness
		# o eliminare gli individui meno adatti.
		pass

class Mutation(object):
	pass

class AlphabeticMutation(Mutation):
	def mutate_single_char(self):
		"""
		substitute a single position with a random char
		"""
		pass
	
	def mutate_chars_with_probability(self, prob):
		"""
		sustitute each position with a random char with probability "prob"
		"""
		pass

	def mutate_invert(self):
		"""
		invert the string
		"""
		pass

	def mutate_switch(self):
		"""
		pick a random position x and returns sequence[:x] + sequence[x:]
		"""
		pass

	def mutate_skip(self):
		"""
		remove a random substring from the string
		"""
		pass


class Crossover(object):
	pass

class AlphabeticCrossover(Crossover):
	def reproduce(self, father, mother):
		pass

class Evolve(object):
	def __init__(self):
		self.population = Population()

	def match(self):
		"""
		pick 2 random individuals, vote them (either via user choice via console, goggole search result, etc), and update the fitness
		"""
		return settings.MATCH_FUNCTION()

	def cycle(self):
		"""
		match between random individuals, or reproduction between individuals chosen accordingly to fitness
		(how to choose between "reproduction" and match? every given number of cycle? with some probability?)
		apply mutation (with some probability) to newborns
		"""
		while True:
			couple = self.population.choose_random_couple()
			try:
				winner = self.match(couple)
			except InterruptException: # Definire un'eccezione che interrompe la simulazione
				break
			if chance(settings.REPRODUCTION_RATE):
				offspring = settings.RECOMBINE_FUNCTION(self.population.choose_random_couple(by_fitness = True))
				for individual in offspring:
					if chance(settings.MUTATION_PROBABILITY):
						individual.mutate()
					self.population.append(individual)
			self.population.prune()

# Funzione ausiliarie
def chance(probability = 0.5):
	"""
	Returns true probability*100 times out of 100 calls
	"""
	return random.random() < probability
