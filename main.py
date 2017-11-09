#!/usr/bin/env python3
import os
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.fork_manager import ForkManager
from source.genome import Genome


def output(simulation_number, resources, speed, time, iod, genome):
    os.makedirs('output/', exist_ok=True)
    os.makedirs('output/simulation_{}/'.format(simulation_number))

    with open("output/simulation_{}/cell.txt".format(simulation_number), 'w')\
            as output_file:
        output_file.write("{}\t{}\t{}\t{}\t\n".format(resources,
                                                      speed,
                                                      time,
                                                      iod))

    for chromosome in genome:
        with open("output/simulation_{}/{}.txt".format(simulation_number, chromosome.code), 'w') as output_file:
            output_file.write(str(chromosome))


def main(args):
        chromosomes = [Chromosome(**d) for d in args['chromosome_data']]
        genome = Genome(chromosomes=chromosomes)
        fork_manager = ForkManager(size=args['number_of_resources'], genome=genome, speed=args['replication_speed'])
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

        output(simulation_number=args['simulation_number'],
               resources=j,
               speed=k,
               time=time,
               iod=genome.average_interorigin_distance(),
               genome=genome)


if __name__ == '__main__':
    number_of_repetitions = int(sys.argv[sys.argv.index('--cells') + 1])
    organism = sys.argv[sys.argv.index('--organism') + 1]

    data_manager = DataManager(database_path='data/simulation.sqlite',
                               mfa_seq_folder_path='data/MFA-Seq_TBrucei_TREU927/')
    chromosome_data = data_manager.chromosomes(organism=organism)
    number_of_resources_range = (int(sys.argv[sys.argv.index('--resources') + 1]),
                                 int(sys.argv[sys.argv.index('--resources') + 2]),
                                 int(sys.argv[sys.argv.index('--resources') + 3]))
    replication_fork_speed_range = (int(sys.argv[sys.argv.index('--speed') + 1]),
                                    int(sys.argv[sys.argv.index('--speed') + 2]),
                                    int(sys.argv[sys.argv.index('--speed') + 3]))

    args_list = []
    l = 0
    for i in range(*number_of_resources_range):
        for j in range(*replication_fork_speed_range):
            for k in range(number_of_repetitions):
                args_list.append({'chromosome_data': chromosome_data,
                                  'number_of_resources': i,
                                  'replication_speed': j,
                                  'simulation_number': l})
                l += 1

    Pool(processes=40).map(main, args_list)
