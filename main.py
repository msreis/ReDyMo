#!/usr/bin/env python3

""" This file is part of ReDyMo.

    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.
    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.
    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.

"""


import os
import shutil
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.fork_manager import ForkManager
from source.genome import Genome


def output(simulation_number, resources, speed, time, iod, genome):

    # Erase results from a previous simulation.
    #
    if os.path.isdir('output/'):
      shutil.rmtree('output/')

    # Prepare directories for this simulation.
    #
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
        period = args['transcription_period']
        simulation_timeout = args['timeout']
  
        print('[done]\n')
        sys.stdout.flush()

        time = 0
       
        number_of_collisions = 0

        print('Starting simulation...')
        sys.stdout.flush()

        while not genome.is_replicated() and simulation_timeout > 0:

            time += 1

            simulation_timeout -= 1

            # Advance replisomes.
            #
            fork_manager.advance_attached_forks(time=time)

            # Check for head-to-head collisions.
            #
            if period > 0:
              number_of_collisions += fork_manager.check_replication_transcription_conflicts(time=time, period=period)

            # One attempt for each unattached fork (this number can be changed)
            #
            for attempt in range(fork_manager.number_of_free_forks):
                genomic_location = genome.random_genomic_location()
                if not genomic_location.is_replicated()\
                        and genomic_location.will_activate()\
                        and fork_manager.number_of_free_forks >= 2:
                    fork_manager.attach_forks(genomic_location=genomic_location, time=time)


        print('[done]\n')
        print('Number of head-to-head collisions: ' + str(number_of_collisions) + '\n')
        sys.stdout.flush()

        output(simulation_number=args['simulation_number'],
               resources=args['number_of_resources'],
               speed=args['replication_speed'],
               time=time,
               iod=genome.average_interorigin_distance(),
               genome=genome)


if __name__ == '__main__':

    number_of_repetitions = int(sys.argv[sys.argv.index('--cells') + 1])

    organism = sys.argv[sys.argv.index('--organism') + 1]

    data_manager = DataManager(database_path='data/simulation.sqlite',
                               mfa_seq_folder_path='data/MFA-Seq_TBrucei_TREU927/')

    number_of_resources_range = (int(sys.argv[sys.argv.index('--resources') + 1]),
                                 int(sys.argv[sys.argv.index('--resources') + 2]),
                                 int(sys.argv[sys.argv.index('--resources') + 3]))

    replication_fork_speed_range = (int(sys.argv[sys.argv.index('--speed') + 1]),
                                    int(sys.argv[sys.argv.index('--speed') + 2]),
                                    int(sys.argv[sys.argv.index('--speed') + 3]))

    transcription_period = (int(sys.argv[sys.argv.index('--period') + 1]))

    simulation_timeout = (int(sys.argv[sys.argv.index('--timout') + 1]))


    # Load data from database.
    #
    print('Loading data... ')
    sys.stdout.flush()

    chromosome_data = data_manager.chromosomes(organism=organism)

    args_list = []
    l = 0
    for i in range(*number_of_resources_range):
        for j in range(*replication_fork_speed_range):
            for k in range(number_of_repetitions):
                args_list.append({'chromosome_data': chromosome_data,
                                  'number_of_resources': i,
                                  'replication_speed': j,
                                  'simulation_number': l,
                                  'timeout': simulation_timeout,
                                  'transcription_period': transcription_period})
                l += 1

    Pool(processes=40).map(main, args_list)


