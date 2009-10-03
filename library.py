import settings
import random
import genoken

class Encoding():
    """
    Represents the encoding of an individual.
    Subclasses implement actual mutate and recombine method
    """
    def mutate(self):
        raise NotImplementedError

    def recombine(self, other):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError

class Fitness():
    def __float__(self):
        raise NotImplementedError
    
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
        raise NotImplementedError

    def lose(self, by = None):
        raise NotImplementedError


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
        if char is not submitted a random char is chosen
        """
        i = random.randrange(len(self.sequence))
        if char == None: char = random.choice(settings.ALPHABET)
        self.sequence = self.sequence[:i] + char + self.sequence[i+1:]

    def mutate_chars_with_probability(self, prob):
        """
        sustitute each position with a random char with probability "prob"
        """
        if prob == None:
            prob = float(1) / float(len(self))
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
        return (AlphabeticEncoding(self.sequence[:i] + other.sequence[j:]),
                AlphabeticEncoding(other.sequence[:j] + self.sequence[i:]))

    def recombine(self, other):
        return self.single_point_crossover(other)

    def mutate(self):
        c = random.randint(0,4)
        if c == 0:
            return self.mutate_single_char()
        elif c == 1:
            return self.mutate_chars_with_probability()
        elif c == 2:
            return self.mutate_invert()
        elif c == 3:
            return self.mutate_switch()
        elif c == 4:
            return self.mutate_skip()

class WonPlayedFitness(Fitness):
    def __init__(self):
        self.won = 0.0
        self.played = 0.0
    
    def __float__(self):
        return (float(self.won) / float(self.played)) + 1 if self.played != 0 else 0.0

    def win(self, over = None):
        self.won += 1
        self.played += 1

    def lose(self, by = None):
        self.played += 1

# Funzione ausiliarie
def chance(probability = 0.5):
    """
    Returns true probability*100 times out of 100 calls
    """
    return random.random() < probability

def choose_with_probability(population):
    """
    The argument is a list of float. Each element is the 
    probability to choose this one plus the probability of
    the previous ones.
    Returns the index of the choosen element.
    """
    choose = random.random() * population.total_fitness()
    sum = 0
    for individual in population:
        sum += individual.get_fitness()
        if choose < sum:
            return individual

# Match functions
def console_match(couple):
    #from genoken import StopEvolving
    print "Which is more meaningful? (add '+' for a stronger vote)"
    print "1) %s" % couple[0]
    print "2) %s" % couple[1]
    print "3) end"
    input = raw_input()
    try:
        vote = input[0]
        try:
            strong = (input[1] == '+')
        except IndexError:
            strong = False
        if vote == "1":
            return (couple[0], couple[1])
        elif vote == "2":
            return (couple[1], couple[0])
        elif vote == "3":
            raise genoken.StopEvolving
    except IndexError:
        pass
