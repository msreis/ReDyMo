#!/usr/bin/env python3
import sys

from chromosome import Chromosome
from database import Database
from fork_manager import ForkManager
from genome import Genome

organism = sys.argv[sys.argv.index('--organism') + 1]
number_of_resources = (int(sys.argv[sys.argv.index('--resources') + 1]),
                       int(sys.argv[sys.argv.index('--resources') + 2]),
                       int(sys.argv[sys.argv.index('--resources') + 3]))
number_of_cells = int(sys.argv[sys.argv.index('--cells') + 1])
with Database('simulation.sqlite') as db:
    chromosome_data = db.select_chromosomes(organism=organism)

for i in range(number_of_cells):
    for j in range(*number_of_resources):
        chromosomes = [Chromosome(t[0], t[1]) for t in chromosome_data]
        genome = Genome(chromosomes=chromosomes)
        fork_manager = ForkManager(size=j, genome=genome)
        time = 0

        while not genome.is_replicated():
            fork_manager.advance_attached_forks()

            attempts = fork_manager.number_of_unattached_forks
            for attempt in range(attempts):   # IMPROVEMENT: Stop loop when out of unattached forks
                genomic_location = genome.random_genomic_location()
                if not genomic_location.is_replicated() and genomic_location.will_activate():
                    fork_manager.attach_forks(genomic_location=genomic_location)

            time += 1
