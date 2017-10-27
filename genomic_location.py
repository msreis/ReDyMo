import random


class GenomicLocation:
    def __init__(self, base, chromosome):
        self.base = base
        self.chromosome = chromosome

    def is_replicated(self):
        return self.chromosome.base_is_replicated(base=self.base)

    def will_activate(self):
        return random.random() < self.chromosome.activation_probability(base=self.base)
