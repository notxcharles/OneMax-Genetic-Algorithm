import random
import csv

from individual import Individual
import config

class GA:
	file_name = "tournament_with_elites.csv"

	def __init__(self):
		self.population: list[Individual] = self.generate_first_gen_individuals()
		self.highest_fitness = max([individual.get_fitness_score() for individual in self.population])
		self.current_generation: int = 1

		with open(self.file_name, mode="wt", newline="\n") as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow([
				"GenerationNumber",
				"TotalFitness",
				"AverageFitness",
				"HighestFitness",
				"PopulationSize",
			])

		self.start_algorithm()

	def generate_first_gen_individuals(self):
		"""Generate the first generation of individuals

		:return: Returns the population, a list of individuals
		"""
		pop: list[Individual] = []

		for _ in range(config.MAX_GENERATIONS):
			indiv = Individual()
			pop.append(indiv)

		return pop

	def tournament_selection(self) -> Individual:
		"""Performs tournament selection

		We select /config.TOURNAMENT_SELECTION_PERCENT/ of the population and then select the individual with the highest fitness

		:rtype: Individual
		:return: Returns the fittest individual
		"""
		tournament_size: int = int(config.TOURNAMENT_SELECTION_PERCENT * len(self.population))
		tournament_population: list[Individual] = random.sample(self.population, tournament_size)
		tournament_scores: list[int] = [individual.get_fitness_score() for individual in tournament_population]

		highest_score: int = -1
		highest_individual: Individual = None

		for i, individual in enumerate(tournament_population):
			individual_score: int = tournament_scores[i]
			if individual_score > highest_score:
				highest_score = individual_score
				highest_individual = individual

		return highest_individual

	def create_new_generation_tournament(self) -> None:
		"""Creates a new generation of individuals, using a tournament selection process

		:return: None
		"""
		children = []

		elites = self.select_best(config.ELITES_SIZE)
		for elite in elites:
			children.append(elite)

		size = len(self.population) - config.ELITES_SIZE

		for i in range(0, len(self.population) - config.ELITES_SIZE, 2):
			parent_a = self.tournament_selection()
			parent_b = self.tournament_selection()

			child_a, child_b = self.breed_individuals(parent_a, parent_b)

			children.append(child_a)
			children.append(child_b)

		self.population = children
		return

	def select_best(self, k=2):
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

		Uses a fixed crossover point /config.CROSSOVER_POINT/ to decide how much of each parents' chromosomes to share with the other

		:param parent_a: Individual A
		:param parent_b: Individual B
		:rtype: tuple[Individual, Individual]
		:return:
		"""
		c_point: int = config.CROSSOVER_POINT

		parent_a_chromosome: list[int] = parent_a.chromosome
		parent_b_chromosome: list[int] = parent_b.chromosome

		child_a_chromosome: list[int] = parent_a_chromosome[:c_point] + parent_b_chromosome[c_point:]
		child_b_chromosome: list[int] = parent_b_chromosome[:c_point] + parent_a_chromosome[c_point:]

		child_a: Individual = Individual(child_a_chromosome)
		child_b: Individual = Individual(child_b_chromosome)

		child_a.mutation()
		child_b.mutation()

		return (child_a, child_b)

	def save_generation_statistics(self, statistics: list[int | float]):
		with open(self.file_name, mode='a', newline="\n") as csv_file:
			writer = csv.writer(csv_file)
			generation, total, average, highest, popsize = statistics
			writer.writerow([generation, total, average, highest, popsize])
		return

	def get_generation_statistics(self):
		highest_fitness = max([individual.get_fitness_score() for individual in self.population])
		total_fitness = sum([individual.get_fitness_score() for individual in self.population])
		average_fitness = total_fitness / len(self.population)
		print(
			f"{self.current_generation}: {total_fitness=}, {average_fitness=}, {highest_fitness=}, {len(self.population)=}")
		return [self.current_generation, total_fitness, average_fitness, highest_fitness, len(self.population)]

	def start_algorithm(self):
		stats = self.get_generation_statistics()
		self.save_generation_statistics(stats)
		while ((self.current_generation <= config.MAX_GENERATIONS) & (self.highest_fitness < int(config.CHROMOSOME_LENGTH))):
			self.create_new_generation_tournament()
			self.current_generation += 1
			self.highest_fitness = max([individual.get_fitness_score() for individual in self.population])
			stats = self.get_generation_statistics()
			self.save_generation_statistics(stats)


for i in range(250):
	ga = GA()