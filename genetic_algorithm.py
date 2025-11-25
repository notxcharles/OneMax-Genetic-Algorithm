import random

from individual import Individual
import config

class GA():
	population_size = config.POPULATION_SIZE
	tournament_selection_percent = config.TOURNAMENT_SELECTION_PERCENT
	crossover_point = config.CROSSOVER_POINT


	def __init__(self):
		self.population: list[Individual] = self.generate_first_gen_individuals()
		print(self.population)
		print([indiv.get_fitness_score() for indiv in self.population])
		self.create_new_generation()
		print("new generation:")
		print(self.population)
		print([indiv.get_fitness_score() for indiv in self.population])


	def generate_first_gen_individuals(self):
		pop: list[Individual] = []

		for _ in range(self.population_size):
			indiv = Individual()
			pop.append(indiv)

		return pop

	def tournament_selection(self) -> Individual:
		"""Pick k random individuals. From those k individuals, select the best."""
		tournament_size: int = int(self.tournament_selection_percent * self.population_size)
		tournament_population: list[Individual] = random.sample(self.population, tournament_size)
		tournament_scores: list[int] = [individual.get_fitness_score() for individual in tournament_population]

		# print(f"{tournament_population=}")
		# print(f"{tournament_scores=}")

		highest_score: int = -1
		highest_individual: Individual = None

		for i, individual in enumerate(tournament_population):
			individual_score: int = tournament_scores[i]
			if individual_score > highest_score:
				highest_score = individual_score
				highest_individual = individual

		return highest_individual

	def create_new_generation(self):
		"""Given the current population, create the new generation"""

		elites = self.select_best(config.ELITES_SIZE)
		children = []

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
		elites = []

		pop = self.population.copy()
		pop_scores = [individual.get_fitness_score() for individual in pop]
		for _ in range(k):
			highest_score: int = -1
			highest_score_i: int = 0
			highest_individual: Individual = None

			for i, individual in enumerate(pop):
				individual_score: int = pop_scores[i]
				if individual_score > highest_score:
					highest_score = individual_score
					highest_score_i = i
					highest_individual = individual

			pop.pop(highest_score_i)
			pop_scores.pop(highest_score_i)
			elites.append(highest_individual)
		return elites

	def breed_individuals(self, parent_a: Individual, parent_b: Individual):
		parent_a_chromosome = parent_a.chromosome
		parent_b_chromosome = parent_b.chromosome

		child_a_chromosome = parent_a_chromosome[:self.crossover_point] + parent_b_chromosome[self.crossover_point:]
		child_b_chromosome = parent_b_chromosome[:self.crossover_point] + parent_a_chromosome[self.crossover_point:]

		child_a = Individual(child_a_chromosome)
		child_b = Individual(child_b_chromosome)

		child_a.mutation()
		child_b.mutation()

		return (child_a, child_b)


ga = GA()