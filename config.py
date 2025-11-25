# Individuals
# One of the stopping criteria is a chromosome of [1] * CHROMOSOME_LENGTH
CHROMOSOME_LENGTH = 10

# When a new individual is randomly created, what is the chance that one of their genes will be a 1
CHROMOSOME_GENERATION_1_CHANCE = 0.1


POPULATION_SIZE = 100

MAX_GENERATIONS = 100

# Using elites selection, how many of the fittest individual qualify as elites?
ELITES_SIZE = 2
# percentage of the population for the tournament, 0.2=20%
TOURNAMENT_SELECTION_PERCENT = 0.2


CROSSOVER_POINT = 5
# Percentage, 0.01 = 1%
MUTATION_CHANCE = 0.01