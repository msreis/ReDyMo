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

  os.makedirs(directory + simulation, exist_ok=True)

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
  origins_range = args['origins_range']

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

  # Set the flag of constitutive origins.
  #
  use_constitutive_origins = False
  if origins_range > 0:
    use_constitutive_origins = True


  print('Starting simulation...', end='')
  sys.stdout.flush()

  while not genome.is_replicated() and simulation_timeout > 0\
  and not (number_of_constitutive_origins == 0 and \
  fork_manager.number_of_free_forks == fork_manager.number_of_forks):
  
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
        and fork_manager.number_of_free_forks >= 2\
        and genomic_location.will_activate(use_constitutive_origins,\
                                           origins_range):

          fork_manager.attach_forks(genomic_location=genomic_location,time=time)

          if use_constitutive_origins == True:
            origin = genomic_location.get_constitutive_origin(origins_range)
            if genomic_location.put_fired_constitutive_origin(origin) == False:
              print('Error in putting fired constitutive origin!')         
            number_of_constitutive_origins -= 1

  print('[done]')
  if genome.is_replicated():
    print('Genome was successfully duplicated!')
  elif simulation_timeout == 0:
    print('WARNING: Simulation timeout reached!')
  print('Number of head-to-head collisions: ' + str(number_of_collisions))
  if use_constitutive_origins == True:
    print('Number of constitutive origins that did not fire: ' +\
    str(number_of_constitutive_origins))

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

  # Check whether all mandatory arguments are present.
  #
  if '--cells' not in sys.argv[1:] or '--organism' not in sys.argv[1:] or\
     '--resources' not in sys.argv[1:] or '--speed' not in sys.argv[1:] or\
     '--timeout' not in sys.argv[1:]:
     
    print('Insufficient number of arguments (see README.md).')
    sys.exit()

  number_of_repetitions = int(sys.argv[sys.argv.index('--cells') + 1])
  organism = sys.argv[sys.argv.index('--organism') + 1]
  data_manager = DataManager(database_path='data/simulation.sqlite',
                 mfa_seq_folder_path='data/MFA-Seq_TBrucei_TREU927/')
  number_of_resources = (int(sys.argv[sys.argv.index('--resources') + 1]))
  replication_fork_speed = (int(sys.argv[sys.argv.index('--speed') + 1]))
  simulation_timeout = (int(sys.argv[sys.argv.index('--timeout') + 1]))


  # transcription_period == 0 means that this simulation will be carried out 
  # without constitutive transcription activation.
  #
  transcription_period = 0
  if '--period' in sys.argv[1:]:
    transcription_period = (int(sys.argv[sys.argv.index('--period') + 1]))

  
  # origins_range > 0 means that in this simulation it will be used 
  # constitutive origins only, with a range of 'origins_range' Kb per origin.
  #
  origins_range = 0
  if '--constitutive' in sys.argv[1:]:
    origins_range = (int(sys.argv[sys.argv.index('--constitutive') + 1]))

  # 'False' or 'True'
  #
  if (sys.argv[sys.argv.index('--dormant') + 1] == 'True'):
    dormant_flag = True
  elif (sys.argv[sys.argv.index('--dormant') + 1] == 'False'):
    dormant_flag = False
  else:
    print('Error: --dormant parameter must be either False or True.\n')
    sys.exit()

  # Load data from database.
  #
  print('Loading data... ', end='')
  sys.stdout.flush()

  chromosome_data = data_manager.chromosomes(organism=organism)

  print('[done]')
  sys.stdout.flush()

  args_list = []

  for k in range(number_of_repetitions):

    # Once the dormant origins assay modifies the probability
    # landscape, for that type of experiment we need to load
    # the original landscape again.
    #
    if dormant_flag == True:
      chromosome_data = data_manager.chromosomes(organism=organism)

    args_list.append({  'origins_range': origins_range,
                      'chromosome_data': chromosome_data,
                  'number_of_resources': number_of_resources,
                    'replication_speed': replication_fork_speed,
                    'simulation_number': k,
                              'timeout': simulation_timeout,
                          'has_dormant': dormant_flag,
                 'transcription_period': transcription_period})

  Pool(processes=number_of_processes).map(main, args_list)

#-----------------------------------------------------------------------------#
