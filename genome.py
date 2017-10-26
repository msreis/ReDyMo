from random import Random
from genomic_location import GenomicLocation


class Genome:
    rng = Random()

    def __init__(self, chromosomes):
        self.chromosomes = chromosomes

    def random_genomic_location(self):
        random_chromosome = self.chromosomes[self.rng.randint(0, len(self.chromosomes) - 1)]
        random_base = self.rng.randint(0, len(random_chromosome) - 1)
        return GenomicLocation(random_base, random_chromosome)

    def is_replicated(self):    # IMPROVEMENT: Use a variable to remember amount of replicated chromosomes
        return all([chromosome.is_replicated() for chromosome in self.chromosomes])
