#!/usr/bin/env python3
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.fork_manager import ForkManager

from source.genome import Genome


def main(args):
    number_of_resources = (int(sys.argv[sys.argv.index('--resources') + 1]),
                           int(sys.argv[sys.argv.index('--resources') + 2]),
                           int(sys.argv[sys.argv.index('--resources') + 3]))
    replication_fork_speed = (int(sys.argv[sys.argv.index('--speed') + 1]),
                              int(sys.argv[sys.argv.index('--speed') + 2]),
                              int(sys.argv[sys.argv.index('--speed') + 3]))
    with open("output/cell_{}.txt".format(args[1]), 'w') as output_file:
        for j in range(*number_of_resources):
            for k in range(*replication_fork_speed):
                chromosomes = [Chromosome(**d) for d in args[0]]
                genome = Genome(chromosomes=chromosomes)
                fork_manager = ForkManager(size=j, genome=genome, speed=k)
                time = 0

                while not genome.is_replicated():
                    fork_manager.advance_attached_forks()

                    # One attempt for each unattached fork (this number can be changed)
                    for attempt in range(fork_manager.number_of_free_forks):
                        genomic_location = genome.random_genomic_location()
                        if not genomic_location.is_replicated()\
                                and genomic_location.will_activate()\
                                and fork_manager.number_of_free_forks >= 2:
                            fork_manager.attach_forks(genomic_location=genomic_location)

                    time += 1

                output_file.write("{}\t{}\t{}\t{}\t\n".format(j,
                                                              k,
                                                              time,
                                                              genome.average_interorigin_distance()))
                output_file.flush()

if __name__ == '__main__':
    number_of_cells = int(sys.argv[sys.argv.index('--cells') + 1])
    organism = sys.argv[sys.argv.index('--organism') + 1]

    data_manager = DataManager(database_path='data/simulation.sqlite',
                               mfa_seq_folder_path='data/MFA-Seq_TBrucei_Senoid/')
    chromosome_data = data_manager.chromosomes(organism=organism)
    args_list = []
    for i in range(number_of_cells):
        args_list.append((chromosome_data, i))

    Pool(processes=40).map(main, args_list)
