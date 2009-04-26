class config(object):
	"""
	various configuration parameters
	"""
	ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
	MUTATION_PROBABILITY = 0.01
	REPRODUCTION_RATE = 0.2
	POPULATION_SIZE = 1000
	INDIVIDUAL_TYPE = "AlphabeticIndividual"


class Individual(object):
	pass

class AlphabeticIndividual(Individual):
	def __init__(self, max_length=10):
		self.sequence=''
		alphabet_length=len(ALPHABET)
		length=random.randint(0, max_length)
		for i in range(length):
			self.sequence+=ALPHABET[random.randint(0, alphabet_length)]
		self.played = 0
		self.won = 0

	def __init__(self, sequence):
		self.sequence = sequence
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
	pool = []
	def init_population(self, size, individual_type=AlphabeticIndividual):
		for i in range(size):
			self.pool.append(individual_type())
			

	def choose_random_individual(self):
		return random.choose(self.pool)

	def choose_linear_probability_fitness_individual(self):
		"""
		return an individual according to fitness
		--problem: how to deal with fitness=0? ...beware how fitness is evaluated!
		"""
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
		self.population = Population(config.POPULATION_SIZE, config.INDIVIDUAL_TYPE)

	def match(self):
		"""
		pick 2 random individuals, vote them (either via user choice via console, goggole search result, etc), and update the fitness
		"""
		pass

	def cycle(self):
		"""
		match between random individuals, or reproduction between individuals chosen accordingly to fitness
		(how to choose between "reproduction" and match? every given number of cycle? with some probability?)
		apply mutation (with some probability) to newborns
		"""
		pass
