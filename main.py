#!/usr/bin/env python3
import os
import sys
from multiprocessing import Pool

from source.chromosome import Chromosome
from source.data_manager import DataManager
from source.genome import Genome
from source.transcription_region import TranscriptionRegion


def output(sim_number, resources, speed, period, time, iod, percentage_log, genome):
    os.makedirs('output/', exist_ok=True)
    os.makedirs('output/simulation_{}/'.format(sim_number))

    with open("output/simulation_{}/cell.txt".format(sim_number), 'w')\
            as output_file:
        output_file.write("{}\t{}\t{}\t{}\t{}\t\n".format(resources,
                                                          speed,
                                                          period,
                                                          time,
                                                          iod))

    with open("output/simulation_{}/replication_percentage.txt".format(sim_number), 'w') as output_file:
        for log in percentage_log:
            output_file.write("{}\t{}\t{}\t\n".format(*log))

    for chromosome in genome:
        with open("output/simulation_{}/{}.txt".format(sim_number, chromosome.code), 'w') as output_file:
            output_file.write(str(chromosome.replication_status()))

        with open("output/simulation_{}/{}_conflicts.txt".format(sim_number, chromosome.code), 'w') as output_file:
            output_file.write(str(chromosome.conflict_status()))


def main(args):
        chromosomes = []
        for data in args['chromosome_data']:
            transcription_regions = []
            for region_data in data['transcription_regions']:
                transcription_regions.append(TranscriptionRegion(start=region_data['start'],
                                                                 end=region_data['end'],
                                                                 period=args['transcription_period'],
                                                                 speed=int(2*args['replication_speed']/3)))
            chromosomes.append(Chromosome(code=data['code'],
                                          length=data['length'],
                                          probability_landscape=data['probability_landscape'],
                                          replication_speed=args['replication_speed'],
                                          transcription_regions=transcription_regions))

        genome = Genome(chromosomes=chromosomes, resources=args['number_of_resources'])
        time = 0
        interval = 1
        time_limit = int(1.25 * 8300)
        percentage_log = list()

        while not time > time_limit and genome.replication_percentage() < 1:
            percentage_log.append((time, genome.replication_percentage(), genome.average_interorigin_distance()))

            time += interval

            genome.advance_replication_forks(interval=interval, time=time)

            genome.advance_transcription_forks(interval=interval)

            genome.attach_transcription_forks(interval=interval)

            genome.attach_replication_forks()

        output(sim_number=args['simulation_number'],
               resources=args['number_of_resources'],
               speed=args['replication_speed'],
               period=args['transcription_period'],
               time=time,
               iod=genome.average_interorigin_distance(),
               percentage_log=percentage_log,
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

    transcription_period_range = (int(sys.argv[sys.argv.index('--period') + 1]),
                                  int(sys.argv[sys.argv.index('--period') + 2]),
                                  int(sys.argv[sys.argv.index('--period') + 3]))

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

    Pool(processes=40).map(main, args_list)
