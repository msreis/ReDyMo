""" This file is part of ReDyMo.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>. """

from random import Random


class Genome:
    rng = Random()

    def __init__(self, chromosomes, resources):
        self.chromosomes = chromosomes
        for chromosome in self.chromosomes:
            chromosome.genome = self
        self.resources = resources

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
        return random_base, random_chromosome

    def is_replicated(self, threshold):
        return self.replication_percentage() >= threshold

    def replication_percentage(self):
        total_replicated_bases = 0
        for chromosome in self:
            total_replicated_bases += chromosome.number_of_replicated_bases

        return float(total_replicated_bases/len(self))

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

    def attach_transcription_forks(self, interval):
        for chromosome in self:
            chromosome.attach_transcriptions(interval=interval)

    def attach_replication_forks(self):
        for attempt in range(self.resources):
            if self.resources >= 2:
                random_base, random_chromosome = self.random_genomic_location()
                random_chromosome.attach_replication(base=random_base)

    def advance_transcription_forks(self, interval):
        for chromosome in self:
            self.resources += chromosome.advance_transcriptions(interval=interval)

    def advance_replication_forks(self, interval, time):
        for chromosome in self:
            self.resources += chromosome.advance_replications(interval=interval, time=time)
