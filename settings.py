import library

MUTATION_PROBABILITY = 0.01
REPRODUCTION_RATE = 0.2
POPULATION_SIZE = 1000
ENCODING_TYPE = library.AlphabeticEncoding
FITNESS_TYPE = library.WonPlayedFitness
MATCH_FUNCTION = library.google_match # library.console_match
CHOOSE_INDIVIDUAL_BY_FITNESS = library.choose_with_probability

# Alphabetic settings
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
MAX_ALPHABETIC_INDIVIDUAL_INIT_LENGTH = 10
