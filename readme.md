# OneMax Genetic Algorithm
The goal is to find a binary string of a given length that contains all ones, thereby maximizing the sum of its digits, using a genetic algorithm

## Population
A population is a set of candidate solutions (set of individuals).

In this problem, each individual will be represented by an array of length n

eg [0,0,0,0,0]

## Fitness Function
The fitness function measures the quality of each individual.

eg:
- [0,0,0,0,0] has a fitness score of 0
- [1,1,1,1,1] has a fitness score of 5

## Selection
Individuals with a higher fitness are more likely to reproduce

## Reproduction
We can combine parts of parents to create offspring

eg: Two individuals with fitness scores of 2 and a crossover point of 2:
- a: [1,1,0,0,0]
- b: [0,0,0,1,1]
- child: [1,1,0,1,1]

## Mutation
We may randomly alter parts of an individual

eg: Every generation, a random gene has a chance to change:
- Generation 0: [0,0,0,0,0]
- Generation 10: [0,0,0,0,1]