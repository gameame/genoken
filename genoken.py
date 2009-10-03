import random
import settings
from library import chance

class Individual(object):
    def __init__(self, sequence = None, fitness = None):
        # Controllare che sequence sia di tipo encoding
        self.sequence = sequence if sequence != None else settings.ENCODING_TYPE()
        self.fitness = fitness if fitness != None else settings.FITNESS_TYPE()

    def get_fitness(self):
        return float(self.fitness)

    def recombine(self, other):
        offspring_sequence = self.sequence.recombine(other.sequence)
        return map(lambda x: Individual(sequence = x), offspring_sequence)

    def mutate(self):
        self.sequence.mutate()
        pass

    def __str__(self):
        return str(self.sequence)

    def __len__(self):
        """
        Returns the length of the sequence.
        """
        return len(self.sequence)

    def __cmp__(self, other):
        if other == None:
            return 1
        return cmp(self.get_fitness(), other.get_fitness())

class Population(object):
    """
    Genetic algorithm population management
    """
    def __init__(self, size = settings.POPULATION_SIZE):
        self.pool = []
        self.size = size
        for i in range(size):
            self.pool.append(Individual())

    def choose_random_individual(self, by_fitness = False):
        if by_fitness:
            return settings.CHOOSE_INDIVIDUAL_BY_FITNESS(self)
            # raise NotImplementedError
        else:
            return random.choice(self.pool)

    def choose_random_couple(self, by_fitness = False):
        i1 = self.choose_random_individual(by_fitness = by_fitness)
        while True:
            i2 = self.choose_random_individual(by_fitness = by_fitness)
            if i1 is not i2: break
        return (i1, i2)
    
    def total_fitness(self):
        """
        It sums the fitness of each individual
        """
        #return reduce(lambda x, y: x + y, self.pool)
        return sum(map(lambda i: i.get_fitness(), self.pool))
    
    def sort(self):
        self.pool.reverse()

    def prune(self):
        # TODO Questo metodo dovrebbe essere esguito dopo ogni match
        # e potrebbe riordinare la popolazione in base alla fitness
        # o eliminare gli individui meno adatti.
        self.sort()
        self.pool = self.pool[:self.size]
        #raise NotImplementedError
        #pass

    def append(self, individual):
        self.pool.append(individual)

    def __iter__(self):
        for i in self.pool:
            yield i

    def __str__(self):
        for i in self.pool:
            print "%s, %f" % (i, i.get_fitness())

class Evolve(object):
    def __init__(self):
        self.population = Population()

    def match(self):
        """
        pick 2 random individuals, vote them (either via user choice via console, goggole search result, etc), and update the fitness
        """
        couple = self.population.choose_random_couple()
        winner, loser = settings.MATCH_FUNCTION(couple)
        winner.fitness.win(over = loser.fitness)
        loser.fitness.lose(by = winner.fitness)
        return

    def cycle(self):
        """
        match between random individuals, or reproduction between individuals chosen accordingly to fitness
        (how to choose between "reproduction" and match? every given number of cycle? with some probability?)
        apply mutation (with some probability) to newborns
        """
        # Ho adottato l'opzione probabilita'
        while True:
            try:
                self.match()
            except StopEvolving:
                print self.population
                break
            if chance(settings.REPRODUCTION_RATE):
                individuals = self.population.choose_random_couple(by_fitness = True)
                offspring = individuals[0].recombine(individuals[1])
                for individual in offspring:
                    if chance(settings.MUTATION_PROBABILITY):
                        individual.mutate()
                    self.population.append(individual)
            self.population.prune()

class StopEvolving(Exception):
    pass
