import config
from custom_types import Chromosome
import random



class Individual():
	chromosome_length = config.CHROMOSOME_LENGTH

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
		# if correct_genes = 1, the individual's fitness score is 1

	def generate_random_chromosome(self):
		chromosome = []
		for _ in range(self.chromosome_length):
			if (random.random() < config.CHROMOSOME_GENERATION_1_CHANCE):
				chromosome.append(1)
			else:
				chromosome.append(0)
		return chromosome

	def get_fitness_score(self):
		num_correct_genes = sum(self.chromosome)
		return num_correct_genes

# c: Chromosome = [0,0,0,0,0,0,0,0,0,0]
indiv = Individual()
print(f"{indiv.chromosome}")
print(f"{indiv.get_fitness_score()}")