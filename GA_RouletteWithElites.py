import random
import csv

from individual import Individual
from custom_types import *
import config

class GA_RouletteWithElites:
	def __init__(self, filename: str, iteration: str):
		self.population: list[Individual] = self.generate_first_gen_individuals()
		self.highest_fitness = max([individual.get_fitness_score() for individual in self.population])
		self.current_generation: int = 1

		self.file_name = filename
		self.iteration = iteration

		self.start_algorithm()

	def generate_first_gen_individuals(self) -> list[Individual]:
		"""Generate the first generation of individuals

		:rtype: Individual
		:return: Returns the population, a list of individuals
		"""
		pop: list[Individual] = []

		for _ in range(config.MAX_GENERATIONS):
			indiv = Individual()
			pop.append(indiv)

		return pop

	def roullette_wheel_selection(self) -> Individual:
		"""Perform roulette wheel selection

		An individual is chosen from the population using a roulette wheel. The individual has a higher chance
		if they have a better fitness score

		:rtype: Individual
		:return: One Individual
		"""
		population_scores: list[int] = [individual.get_fitness_score() for individual in self.population]
		return random.choices(self.population, population_scores, k=1)[0]


	def create_new_generation(self) -> None:
		"""Creates a new generation of individuals, using a tournament selection process

		:return: None
		"""
		children = []

		elites = self.elitism_select_best(config.ELITES_SIZE)
		for elite in elites:
			children.append(elite)

		size = len(self.population) - config.ELITES_SIZE

		for i in range(0, size, 2):
			parent_a = self.roullette_wheel_selection()
			parent_b = self.roullette_wheel_selection()

			child_a, child_b = self.breed_individuals(parent_a, parent_b)

			children.append(child_a)
			children.append(child_b)

		self.population = children
		return

	def elitism_select_best(self, k=2) -> list[Individual]:
		"""Select the best individuals from self.population

		:param k: Select k amount of individuals with the highest fitness
		:return: The k best individuals
		"""
		elites = []

		pop_copy = self.population.copy()
		pop_scores = [individual.get_fitness_score() for individual in pop_copy]
		for _ in range(k):
			highest_score: int = -1
			highest_score_i: int = 0
			highest_individual: Individual = None

			for i, individual in enumerate(pop_copy):
				individual_score: int = pop_scores[i]
				if individual_score > highest_score:
					highest_score = individual_score
					highest_score_i = i
					highest_individual = individual

			pop_copy.pop(highest_score_i)
			pop_scores.pop(highest_score_i)
			elites.append(highest_individual)

		return elites

	def breed_individuals(self, parent_a: Individual, parent_b: Individual) -> tuple[Individual, Individual]:
		"""Breeds two individuals' chromosomes.

		Uses a fixed crossover point /config.CROSSOVER_POINT/ to decide how much of each parents'
		chromosomes to share with the other

		:param parent_a: Individual A
		:param parent_b: Individual B
		:rtype: tuple[Individual, Individual]
		:return: two children of parent_a and parent_b
		"""
		c_point: int = config.CROSSOVER_POINT

		parent_a_chromosome: Chromosome = parent_a.chromosome
		parent_b_chromosome: Chromosome = parent_b.chromosome

		child_a_chromosome: Chromosome = parent_a_chromosome[:c_point] + parent_b_chromosome[c_point:]
		child_b_chromosome: Chromosome = parent_b_chromosome[:c_point] + parent_a_chromosome[c_point:]

		child_a: Individual = Individual(child_a_chromosome)
		child_b: Individual = Individual(child_b_chromosome)

		child_a.mutation()
		child_b.mutation()

		return (child_a, child_b)

	def save_generation_statistics(self, statistics: list[int | float], complete=False) -> None:
		"""Saves /statistics/ to self.file_name"""
		with open(self.file_name, mode='a', newline="\n") as csv_file:
			writer = csv.writer(csv_file)
			iteration, generation, total, average, highest, popsize = statistics
			writer.writerow([iteration, generation, total, average, highest, popsize, complete])
		return

	def get_generation_statistics(self) -> list[int | float]:
		"""Generates statistics about the algorithm's current progress

		iteration: how many times previously has this algorithm run
		current_generation: the current generation number
		highest fitness: this generation's individual with the highest fitness
		total_fitness: the total fitness of this generation
		average_fitness: the average fitness of this generation
		population_size: the number of individuals in this generation

		:rtype: list[int | float]
		:return: list of statistics
		"""
		highest_fitness = max([individual.get_fitness_score() for individual in self.population])
		total_fitness = sum([individual.get_fitness_score() for individual in self.population])
		average_fitness = total_fitness / len(self.population)
		print(
			f"{self.iteration=}/{self.current_generation}: {total_fitness=}, {average_fitness=}, "
			f"{highest_fitness=}, {len(self.population)=}")
		return [self.iteration, self.current_generation, total_fitness, average_fitness, highest_fitness, len(self.population)]

	def start_algorithm(self) -> None:
		"""Starts the genetic algorithm until it reaches the stopping criteria"""
		while ((self.current_generation <= config.MAX_GENERATIONS) & (self.highest_fitness < int(config.CHROMOSOME_LENGTH))):
			stats = self.get_generation_statistics()
			self.save_generation_statistics(stats)
			self.create_new_generation()
			self.current_generation += 1
			self.highest_fitness = max([individual.get_fitness_score() for individual in self.population])
		stats = self.get_generation_statistics()
		self.save_generation_statistics(stats, True)
		return

file_name = "roulette_with_elites.csv"

with open(file_name, mode='w', newline="\n") as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow([
		"GAIteration",
		"GenerationNumber",
		"TotalFitness",
		"AverageFitness",
		"HighestFitness",
		"PopulationSize",
		"StoppingConditionReached"
	])

for i in range(1000):
	ga = GA_RouletteWithElites(file_name, f"iteration{i+1}")