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
import argparse

sys.path.append('../')

from ReDyMo.src.chromosome import Chromosome
from ReDyMo.src.data_manager import DataManager
from ReDyMo.src.fork_manager import ForkManager
from ReDyMo.src.genome import Genome

#-----------------------------------------------------------------------------#

def output(simulation_number,dormant,resources,speed,time,iod,genome,period):

  # Prepare directories for this simulation.
  #
  os.makedirs('output', exist_ok=True)

  directory = 'output/' + str(dormant) + '_' +\
              str(resources) + '_' + str(period) + '/'

  os.makedirs(directory, exist_ok=True)

  simulation = 'simulation_{}/'.format(simulation_number)

  os.makedirs(directory + simulation)

  with open(directory + simulation + '/cell.txt', 'w')\
  as output_file:
    output_file.write("{}\t{}\t{}\t{}\t\n".format(resources, speed, time, iod))

  for chromosome in genome:
    code = "{}.txt".format(chromosome.code)
    with open(directory + simulation + code, 'w') as output_file:
      output_file.write(str(chromosome))

#-----------------------------------------------------------------------------#

def main(args):

  chromosomes = [Chromosome(**d) for d in args['chromosome_data']]
  genome = Genome(chromosomes=chromosomes)
  fork_manager = ForkManager(size=args['number_of_resources'],\
                 genome=genome, speed=args['replication_speed'])
  period = args['transcription_period']
  simulation_timeout = args['timeout']
  dormant = args['has_dormant']
  use_constitutive_origins = args['use_constitutive_origins']

  # Parameter that specifies the number of iterations between two
  # different attempts of origin firing (default value == 1).
  #
  alpha = 1
  time = 0

  # Get the number of constitutive origins in the whole genome
  #
  number_of_constitutive_origins = genome.number_of_constitutive_origins()

  # Counter of the total number of head-to-head collisions during a simulation.
  #
  number_of_collisions = 0

  print('Starting simulation...', end='')
  sys.stdout.flush()

  while not genome.is_replicated() and simulation_timeout > 0\
                                   and number_of_constitutive_origins > 0:

    time += 1

    simulation_timeout -= 1

    # Advance replisomes.
    #
    fork_manager.advance_attached_forks(time=time)

    # Check for head-to-head collisions.
    #
    if period > 0:
      number_of_collisions +=\
      fork_manager.check_replication_transcription_conflicts\
      (time=time, period=period, has_dormant=dormant)

    # At an alpha iteration, it makes one attempt for each unattached fork.
    #
    if time % alpha == 0 and not genome.is_replicated():
    
      for attempt in range(fork_manager.number_of_free_forks):
 
        genomic_location = genome.random_genomic_location()

        # This is an alternative to the procedure above, and changes the
        # dynamics of the simulation.
        #
        # genomic_location = genome.random_unreplicated_genomic_location()
 
        if not genomic_location.is_replicated()\
        and genomic_location.will_activate(use_constitutive_origins)\
        and fork_manager.number_of_free_forks >= 2:

          fork_manager.attach_forks(genomic_location=genomic_location,time=time)

          if use_constitutive_origins == True:
            number_of_constitutive_origins -= 1



  print('[done]')
  print('Number of head-to-head collisions: ' + str(number_of_collisions))
  print ('\n')
  sys.stdout.flush()

  output(simulation_number = args['simulation_number'],
                   dormant = dormant,
                 resources = args['number_of_resources'],
                     speed = args['replication_speed'],
                      time = time,
                       iod = genome.average_interorigin_distance(),
                    genome = genome,
                    period = period)

#-----------------------------------------------------------------------------#

if __name__ == '__main__':

  # Maximum number of processes during the parallelized code execution.
  #
  number_of_processes = 40

  # Configure argument parser
  parser = argparse.ArgumentParser(description='Dynamic model of the replication process in kinetoplastida')

  parser.add_argument(
    '--organism',
    dest='organism',
    type=str,
    required=True,
    help=('Organism name, as saved in the database '
          '(remember to add single quotation marks when using space-separated names)')
  )

  parser.add_argument(
    '--cells',
    dest='number_of_repetitions',
    type=int,
    required=True,
    help='Number of independent simulations to be made.',
  )

  parser.add_argument(
    '--resources',
    dest='number_of_resources',
    type=int,
    required=True,
    help='Number of available forks for the replication process.',
  )

  parser.add_argument(
    '--speed',
    dest='replication_fork_speed',
    type=int,
    required=True,
    help='Movement speed of each replication machinery (in bases per second).',
  )

  parser.add_argument(
    '--period',
    dest='transcription_period',
    type=int,
    required=True,
    help='Time between consecutive activations of a transcription region (in seconds).',
  )

  parser.add_argument(
    '--timeout',
    dest='simulation_timeout',
    type=int,
    required=True,
    help=('Maximum allowed number of iterations of a simulation; if this value is reached, '
          'then a simulation is ended even if DNA replication is not completed yet.'),
  )

  parser.add_argument(
    '--dormant',
    dest='dormant_flag',
    type=bool,
    required=True,
    help='Whether dormant origins should be fired.',
  )

  parser.add_argument(
    '--constitutive_origins',
    dest='constitutive_origins_flag',
    type=bool,
    default=True,
    help='Whether constitutive origins should be used.',
  )

  # Parse arguments from command-line
  args = parser.parse_args(sys.argv[1:])

  data_manager = DataManager(database_path='data/simulation.sqlite',
                 mfa_seq_folder_path='data/MFA-Seq_TBrucei_TREU927/')

  # Load data from database.
  #
  print('Loading data... ', end='')
  sys.stdout.flush()

  chromosome_data = data_manager.chromosomes(organism=args.organism)

  print('[done]')
  sys.stdout.flush()

  args_list = []

  for k in range(args.number_of_repetitions):

    # Once the dormant origins assay modifies the probability
    # landscape, for that type of experiment we need to load
    # the original landscape again.
    #
    if args.dormant_flag == True:
      chromosome_data = data_manager.chromosomes(organism=args.organism)

    args_list.append({'chromosome_data': chromosome_data,
                  'number_of_resources': args.number_of_resources,
                    'replication_speed': args.replication_fork_speed,
                    'simulation_number': k,
                              'timeout': args.simulation_timeout,
                          'has_dormant': args.dormant_flag,
             'use_constitutive_origins': args.constitutive_origins_flag,
                 'transcription_period': args.transcription_period})

  Pool(processes=number_of_processes).map(main, args_list)

#-----------------------------------------------------------------------------#
