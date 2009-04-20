"""
This module simulates the evolution of random generated sentences, 
using human feedback to assert if they are meaningful.
"""

import random, cPickle

CUTOFF = 0.005
CROSSING_OVER_COEFF = 0.1
WIN_MUL = 1.5
STRONG_WIN_MUL = 2.0
LOSE_MUL = 0.5
STRONG_LOSE_MUL = 0.25
REMOVE_PROBABILITY = 0.4
REARRANGE_PROBABILITY = 0.4
IMMIGRATION_PROBABILITY = 0.6
COPYERR_PROBABILITY = 0.3
MUTANT_QTY = 0.2
INIT_POOL = "QWERTYUIOPASDFGHJKLZXCVBNM "

class Sentence():
    def __init__(self, sequence, qty = 1.0):
        """
        sequence: the sequence of charcter representing this sentence
        qty: quantity of this sequence in the pool
        """
        self.sequence = sequence
        self.qty = qty

    def win(self, strong = False):
        """
        Call this method when a sentence wins a ballot.
        The quantity of the sentence is increased. There is chance that
        there will be a copy error.
        """
        self.qty *= STRONG_WIN_MUL if strong else WIN_MUL
        if chance(COPYERR_PROBABILITY * self.qty):
            mutant = self.mutate()
            i = random.randrange(0, len(mutant))
            m = random.choice(INIT_POOL)
            mutant.sequence = mutant.sequence[:i] + m + mutant.sequence[i+1:]
            print "mutation: %s > %s (%s)" % (self, mutant, m)

    def lose(self, strong = False):
        """
        Call this method when a sentence lose a ballot.
        """
        self.qty *= STRONG_LOSE_MUL if strong else LOSE_MUL

    def crossing_over(self, other):
        """
        Crossing over replication. No more used
        """
        c = ""
        choose_s = True
        for s, o in zip(self.sequence, other.sequence):
            if random.random() < CROSSING_OVER_COEFF:
                choose_s = not choose_s
            c += s if choose_s else o
        return Sentence(sequence = c)

    def insert(self, sequence):
        """
        Insert a sequence in the sentence, in random position, in straight
        or reverse order.
        """
        if sequence == "": return self.sequence
        if chance(): # reverse sequence
            sequence = reduce(lambda x, y: y + x, sequence)
        i = random.randint(0, len(self.sequence))
        self.sequence = self.sequence[:i] + sequence + self.sequence[i:]

    def extract(self, remove = True):
        """
        Get a random sequence from the sentence.
        If remove == True the sequence will be actually removed 
        from the sentence.
        """
        [begin, end] = sorted([random.randint(0, len(self)),
                               random.randint(0, len(self))])
        sequence = self.sequence[begin:end]
        if remove:
            self.sequence = self.sequence[:begin] + self.sequence[end:]
        return sequence 

    def mutate(self):
        """
        Decrease this sentence quantity by MUTANT_QTY and returns a new 
        sentence with the same sequence and MUTANT_QTY quantity.
        """
        self.qty -= MUTANT_QTY
        return Sentence(self.sequence, qty = MUTANT_QTY)

    def can_survive(self):
        """
        Test if this sentence can survive in the Pool.
        Only sentences with quantity > CUTOFF will survive.
        """
        return True if self.qty > CUTOFF else False

    def __cmp__(self, other):
        """
        Compare by quantity
        """
        if other == None:
            return 1
        return cmp(other.qty, self.qty)

    def __str__(self):
        return '"%s"' % self.sequence
    
    def __len__(self):
        """
        Returns the length of the sequence.
        """
        return len(self.sequence)

    def __float__(self):
        """
        Returns the quantity of the sequence
        """
        return self.qty

    def __add__(self, other):
        """
        Sums quantities
        """
        return self.qty + float(other)

    def __radd__(self, other):
        """
        Sums quantities
        """
        return self.qty + float(other)

class Pool():
    def __init__(self, initial_pool = None):
        """
        Generate a 1-long sentence from each character in initial_pool
        """
        if initial_pool != None:
            self.pool = [Sentence(c) for c in initial_pool]

    def choose_couple(self):
        """
        Randomly chooses two different sentences from the pool.
        """
        # g2 dovrebbe essere scelto simile a g1 per qty?
        g1 = self.choose_one()
        g2 = self.choose_one()
        while (g1 is g2):
            g2 = self.choose_one()
        return (g1, g2)
    
    def choose_one(self, weighted = False, length = None):
        """
        Randomly chooses a sentence from the pool. If weighted == True,
        the quantity of the sentences is taken in account. If length != None
        only sentences with that length will be chosen.
        """
        p = self if length == None else self.slice(length)
        if weighted:
            t = random.random() * p.total_qty()
            i = 0
            s = 0
            while True:
                s += p.pool[i]
                if t < s:
                    break
                i += 1
            return p.pool[i]
        else:
            return random.choice(p.pool)

    def __str__(self):
        return "\n".join(["%s (%f)" % (s, s) for s in sorted(self.pool)])
    
    def __len__(self):
        return len(self.pool)
    
    def total_qty(self):
        """
        Sum of the quantity of the sentences
        """
        return reduce(lambda x, y: x + y, self.pool)
    
    def sort(self):
        self.pool.sort()

    def slice(self, length):
        """
        Return a new Pool containing only the Sentences of the given length
        """
        p = Pool()
        p.pool = filter(lambda x: len(x) == length, self.pool)
        return p

    def count_token(self):
        """
        Returns a report containing all substrings of same length, with 
        """
        report = {}
        for sentence in self.pool:
            for length in xrange(len(sentence)):
                try:
                    report[length + 1]
                except KeyError:
                    report[length + 1] = {}
                for i in xrange(len(sentence) - length):
                    seq = sentence.sequence[i:i+length+1]
                    try:
                        report[length + 1][seq].qty += sentence.qty
                    except KeyError:
                        report[length + 1][seq] = Sentence(sequence = seq, qty = sentence.qty)
        return report

    def append(self, sentence):
        """
        Add sentence to the pool. If a sentence with the same sequence
        already exists, their quantity are summed.  
        """
        if len(sentence) == 0: return
        s = self.find(sentence)
        if s == None:
            self.pool.append(sentence)
        else:
            s.qty += sentence
    
    def find(self, sentence):
        for s in self.pool:
            if s.sequence == sentence.sequence:
                return s
        return None

    def prune(self):
        old_len = len(self.pool)
        self.pool = filter(lambda x: x.can_survive(), self.pool)
        print "pruned %d" % (old_len - len(self.pool))

class Evolve():
    def __init__(self, file_name):
        """
        file_name is the file with the dump of the pool.
        """
        self.file_name = file_name
        try:
            f = open(file_name, "r")
            self.pool = cPickle.load(f)
            f.close()
        except IOError:
            self.pool = Pool(INIT_POOL)

    def ballot(self, s_win, s_lose, strong = False):
        s_win.win(strong = strong)
        s_lose.lose(strong = strong)
    
    def loop(self):
        while True:
            gg = self.pool.choose_couple()
            print
            print "Which is more meaningful? (add '+' for a stronger vote)"
            print "1) %s" % gg[0]
            print "2) %s" % gg[1]
            print "3) end"
            input = raw_input()
            try :
                res = input[0]
                try:
                    strong = (input[1] == "+")
                except IndexError:
                    strong = False
                if res == "1":
                    self.ballot(gg[0], gg[1], strong = strong)
                elif res == "2":
                    self.ballot(gg[1], gg[0], strong = strong)
                elif res == "3":
                    self.stop()
                    break
            except IndexError:
                # if user pass, both lose
                gg[0].lose()
                gg[1].lose()
                
            if chance(REMOVE_PROBABILITY):
                orig = self.pool.choose_one()
                mutant = orig.mutate()
                mutant.extract(remove = True)
                self.pool.append(mutant)
                print "remove: %s > %s" % (orig, mutant)
            if chance(REARRANGE_PROBABILITY):
                orig = self.pool.choose_one()
                mutant = orig.mutate()
                sequence = mutant.extract(remove = True)
                mutant.insert(sequence)
                self.pool.append(mutant)
                print "rearrange: %s > %s" % (orig, mutant)
            if chance(IMMIGRATION_PROBABILITY):
                orig = self.pool.choose_one()
                mutant = orig.mutate()
                migrant = self.pool.choose_one(weighted = True)
                sequence = migrant.extract(remove = False)
                mutant.insert(sequence)
                self.pool.append(mutant)
                print "immigration: %s to %s > %s" % (migrant, orig, mutant)
            self.pool.sort()
            self.pool.prune()

        for length, dict in self.pool.count_token().items():
            print "length %d" % length
            print "=" * len("length %d" % length)
            for sentence in sorted(dict.values()):
                print '%s (%f)' % (sentence, sentence)

    def stop(self):
        f = open(self.file_name, "w")
        cPickle.dump(self.pool, f)
        f.close()

def chance(probability = 0.5):
    """
    Returns true (probability*100) times out of 100 calls
    """
    return random.random() < probability

if __name__ == "__main__":
    Evolve("prova.pic").loop()
