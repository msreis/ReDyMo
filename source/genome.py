""" This file is part of ReDyMo.
    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.
    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.
    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ortra
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.
    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.
"""

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

    def __iter__(self):
        return iter(self.chromosomes)

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

