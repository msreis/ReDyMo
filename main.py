#!/usr/bin/env python3
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.fork_manager import ForkManager

from source.genome import Genome


def output(cell_number, simulation_number, resources, speed, time, iod, genome):
    with open("output/cell_{}-simulation_{}.txt".format(cell_number, simulation_number), 'w')\
            as output_file:
        output_file.write("{}\t{}\t{}\t{}\t\n".format(resources,
                                                      speed,
                                                      time,
                                                      iod))

    with open("output/chromosomes_cell_{}-simulation_{}.txt".format(cell_number, simulation_number), 'w')\
            as output_file:
        for chromosome in genome:
            output_file.write(str(chromosome))


def main(args):
    cell_number = int(args[1])
    number_of_resources = (int(sys.argv[sys.argv.index('--resources') + 1]),
                           int(sys.argv[sys.argv.index('--resources') + 2]),
                           int(sys.argv[sys.argv.index('--resources') + 3]))
    replication_fork_speed = (int(sys.argv[sys.argv.index('--speed') + 1]),
                              int(sys.argv[sys.argv.index('--speed') + 2]),
                              int(sys.argv[sys.argv.index('--speed') + 3]))
    simulation_number = 0
    for j in range(*number_of_resources):
        for k in range(*replication_fork_speed):
            chromosomes = [Chromosome(**d) for d in args[0]]
            genome = Genome(chromosomes=chromosomes)
            fork_manager = ForkManager(size=j, genome=genome, speed=k)
            time = 0

            while not genome.is_replicated():
                time += 1

                fork_manager.advance_attached_forks(time=time)

                # One attempt for each unattached fork (this number can be changed)
                for attempt in range(fork_manager.number_of_free_forks):
                    genomic_location = genome.random_genomic_location()
                    if not genomic_location.is_replicated()\
                            and genomic_location.will_activate()\
                            and fork_manager.number_of_free_forks >= 2:
                        fork_manager.attach_forks(genomic_location=genomic_location, time=time)

            output(cell_number=cell_number,
                   simulation_number=simulation_number,
                   resources=j,
                   speed=k,
                   time=time,
                   iod=genome.average_interorigin_distance(),
                   genome=genome)
            simulation_number += 1


if __name__ == '__main__':
    number_of_cells = int(sys.argv[sys.argv.index('--cells') + 1])
    organism = sys.argv[sys.argv.index('--organism') + 1]

    data_manager = DataManager(database_path='data/simulation.sqlite',
                               mfa_seq_folder_path='data/MFA-Seq_dummy/')
    chromosome_data = data_manager.chromosomes(organism=organism)
    args_list = []
    for i in range(number_of_cells):
        args_list.append((chromosome_data, i))

    Pool(processes=40).map(main, args_list)
