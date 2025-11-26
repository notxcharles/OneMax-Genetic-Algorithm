# OneMax Genetic Algorithm
The goal is to find a binary string of a given length that contains all ones, thereby maximizing the sum of its digits, using a genetic algorithm

## Population
A population is a set of candidate solutions (set of individuals).
- The population size can be changed in the config: `POPULATION_SIZE`

In this problem, each Individual will be represented by an array of length n.

- Currently n=10. This can be changed in the config: `CHROMOSOME_LENGTH`

- eg [0,0,0,0,0]

In the first generation, each individual has a chance to have some genes as 1s.

- This can be changed in the config: `CHROMOSOME_GENERATION_1_CHANCE`

## Fitness Function
The fitness function measures the quality of each individual.

eg:
- [0,0,0,0,0] has a fitness score of 0
- [1,1,1,1,1] has a fitness score of 5

## Selection
Individuals with a higher fitness are more likely to reproduce
### Selection Methods
#### Tournament Selection with Elitism
`GA_TournamentWithElites.py`
- Tournament selection picks a small random subset of individuals from the population (eg, 20%). 
The individual with the highest fitness in that subset wins and is chosen as a parent
  - This can be changed in the config: `TOURNAMENT_SELECTION_PERCENT` 
- Elitism means that a chosen number of the best individuals in the entire population are automatically 
carried over unchanged to the next generation.
  - This can be changed in the config: `ELITES_SIZE`
#### Tournament Selection
`GA_Tournament.py`
- Tournament selection picks a small random subset of individuals from the population (eg, 20%). 
The individual with the highest fitness in that subset wins and is chosen as a parent
  - This can be changed in the config: `TOURNAMENT_SELECTION_PERCENT` 
- There is no elitism in this version
#### Roulette Selection with Elitism
`GA_RouletteWithElites.py`
- Each individual is given a slice of a virtual roulette wheel proportional to its fitness. 
Fitter/better individuals get larger slices.
- Elitism means that a chosen number of the best individuals in the entire population are automatically 
carried over unchanged to the next generation.
  - This can be changed in the config: `ELITES_SIZE`

## Reproduction
We can combine parts of parents to create offspring

eg: Two individuals with fitness scores of 2 and a crossover point of 2:
- a: [1,1,0,0,0], fitness = 2
- b: [0,0,0,1,1], fitness = 2
- child: [1,1,0,1,1], fitness = 4

The crossover point can be changed in the config file: `CROSSOVER_POINT`

## Mutation
We may randomly alter parts of an individual. Every generation, a random gene has a chance to change:
- Generation 0: [0,0,0,0,0]
- Generation 10: [0,0,0,0,1]

This is controlled by the config: `MUTATION_CHANCE`