#!/usr/bin/env python3

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

import os
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.genome import Genome
from source.transcription_region import TranscriptionRegion

""" Skeleton of the simulation process,
    reads the input parameters from standard input,
    starts the parallel simulations and write the results. """


def parse_parameters(command_line_args):
    number_of_repetitions = int(command_line_args[command_line_args.index('--cells') + 1])
    organism = command_line_args[command_line_args.index('--organism') + 1]

    data_manager = DataManager(database_path='data/simulation.sqlite',
                               mfa_seq_folder_path='data/MFA-Seq_TBrucei_TREU927/')
    chromosome_data = data_manager.chromosomes(organism=organism)
    number_of_resources_range = (int(command_line_args[command_line_args.index('--resources') + 1]),
                                 int(command_line_args[command_line_args.index('--resources') + 2]),
                                 int(command_line_args[command_line_args.index('--resources') + 3]))
    replication_fork_speed_range = (int(command_line_args[command_line_args.index('--speed') + 1]),
                                    int(command_line_args[command_line_args.index('--speed') + 2]),
                                    int(command_line_args[command_line_args.index('--speed') + 3]))

    transcription_period_range = (int(command_line_args[command_line_args.index('--period') + 1]),
                                  int(command_line_args[command_line_args.index('--period') + 2]),
                                  int(command_line_args[command_line_args.index('--period') + 3]))

    args_list = []
    simulation_number = 0
    for i in range(*number_of_resources_range):
        for j in range(*replication_fork_speed_range):
            for k in range(*transcription_period_range):
                for l in range(number_of_repetitions):
                    args_list.append({'chromosome_data': chromosome_data,
                                      'number_of_resources': i,
                                      'replication_speed': j,
                                      'transcription_period': k,
                                      'simulation_number': simulation_number})
                    simulation_number += 1

    return args_list


def simulate(args):
    chromosomes = []
    for data in args['chromosome_data']:
        transcription_regions = []
        for region_data in data['transcription_regions']:
            transcription_regions.append(TranscriptionRegion(start=region_data['start'],
                                                             end=region_data['end'],
                                                             period=args['transcription_period'],
                                                             speed=int(2 * args['replication_speed'] / 3)))
        chromosomes.append(Chromosome(code=data['code'],
                                      length=data['length'],
                                      probability_landscape=data['probability_landscape'],
                                      replication_speed=args['replication_speed'],
                                      transcription_regions=transcription_regions))

    genome = Genome(chromosomes=chromosomes, resources=args['number_of_resources'])
    time = 0
    interval = .1
    time_limit = int(1.25 * 8300)
    percentage_log = list()

    while not time > time_limit and genome.replication_percentage() < 1:
        percentage_log.append((time, genome.replication_percentage(), genome.average_interorigin_distance()))

        time += interval

        genome.advance_replication_forks(interval=interval, time=time)

        genome.advance_transcription_forks(interval=interval)

        genome.attach_transcription_forks(interval=interval)

        genome.attach_replication_forks()

    write_results(
                **{'sim_number': args['simulation_number'],
                   'resources': args['number_of_resources'],
                   'speed': args['replication_speed'],
                   'period': args['transcription_period'],
                   'time': time,
                   'iod': genome.average_interorigin_distance(),
                   'percentage_log': percentage_log,
                   'genome': genome}
                 )


def write_results(sim_number, resources, speed, period, time, iod, percentage_log, genome):
    output_folder_path = sys.argv[1]
    os.makedirs(output_folder_path, exist_ok=True)
    os.makedirs(output_folder_path + 'simulation_{}/'.format(sim_number))

    with open(output_folder_path + "simulation_{}/cell.txt".format(sim_number), 'w')\
            as output_file:
        output_file.write("{}\t{}\t{}\t{}\t{}\t\n".format(resources,
                                                          speed,
                                                          period,
                                                          time,
                                                          iod))

    with open(output_folder_path + "simulation_{}/replication_percentage.txt".format(sim_number), 'w') as output_file:
        for log in percentage_log:
            output_file.write("{}\t{}\t{}\t\n".format(*log))

    for chromosome in genome:
        with open(output_folder_path + "simulation_{}/{}.txt".format(sim_number, chromosome.code), 'w') as output_file:
            output_file.write(str(chromosome.replication_status()))

        with open(output_folder_path + "simulation_{}/{}_conflicts.txt".format(sim_number, chromosome.code), 'w') as output_file:
            output_file.write(str(chromosome.conflict_status()))


def main(args):
    simulation_arguments = parse_parameters(command_line_args=args)

    Pool(processes=20).map(simulate, simulation_arguments)


if __name__ == '__main__':
    main(sys.argv)
