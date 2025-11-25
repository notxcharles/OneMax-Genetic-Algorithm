import config
from custom_types import Chromosome
import random


class Individual:
	chromosome_length = config.CHROMOSOME_LENGTH
	mutation_chance = config.MUTATION_CHANCE

	def __init__(self, chromosome: Chromosome = None):
		if chromosome:
			if len(chromosome) != self.chromosome_length:
				raise Exception(f"Chromosome must be of length: {self.chromosome_length}")
			self.chromosome = chromosome
		else:
			self.chromosome = self.generate_random_chromosome()

	def __eq__(self, other):
		"""The individual is equal to their fitness score"""
		num_correct_genes = sum(self.chromosome)
		return num_correct_genes == other

	def __repr__(self):
		return (f"Individual({self.get_fitness_score()})")

	def __str__(self):
		return (f"Individual({self.get_fitness_score()})")

	def generate_random_chromosome(self):
		"""Generate a random chromosome of length: config.CHROMOSOME_LENGTH"""
		chromosome = []
		for _ in range(self.chromosome_length):
			if (random.random() < config.CHROMOSOME_GENERATION_1_CHANCE):
				chromosome.append(1)
			else:
				chromosome.append(0)
		return chromosome

	def get_fitness_score(self):
		"""Fitness score is equal to the number of 1s in the chromosome"""
		num_correct_genes = sum(self.chromosome)
		return num_correct_genes

	def mutation(self):
		"""Perform a mutation if x chance"""
		if random.random() < config.MUTATION_CHANCE:
			i = random.randint(0, len(self.chromosome))
			if self.chromosome[i] == 1:
				self.chromosome[i] = 0
			else:
				self.chromosome[i] = 1
		return


# c: Chromosome = [0,0,0,0,0,0,0,0,0,0]
indiv = Individual()
print(f"{indiv.chromosome}")
print(f"{indiv.get_fitness_score()}")