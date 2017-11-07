from random import Random

from source.genomic_location import GenomicLocation


class Genome:
    rng = Random()

    def __init__(self, chromosomes):
        self.chromosomes = chromosomes

    def __len__(self):
        length = 0
        for chromosome in self.chromosomes:
            length += len(chromosome)

        return length

    def random_genomic_location(self):
        random_chromosome = self.chromosomes[self.rng.randint(0, len(self.chromosomes) - 1)]
        random_base = self.rng.randint(0, len(random_chromosome) - 1)
        return GenomicLocation(base=random_base, chromosome=random_chromosome)

    def is_replicated(self):
        return all([chromosome.is_replicated() for chromosome in self.chromosomes])

    def average_interorigin_distance(self):
        number_of_interorigin_distances = 0
        for chromosome in self.chromosomes:
            number_of_interorigin_distances += chromosome.number_of_origins + 1

        return float(len(self)/number_of_interorigin_distances)

    def number_of_replicated_bases_in_this_step(self):
        number_of_replicated_bases_in_this_step = 0
        for chromosome in self.chromosomes:
            number_of_replicated_bases_in_this_step += chromosome.number_of_recently_replicated_bases

        return number_of_replicated_bases_in_this_step
