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

from ReDyMo.src.replication_fork import ReplicationFork

from array import *


## @package ReDyMo.src.fork_manager
# Contains the class ForkManager.


## This class manages all forks from a genome.
# 
# It stores the replicaton forks and handles attachments, transcription 
# conflicts and fork motion.
class ForkManager:

  ## The class constructor
  def __init__(self, size, genome, speed):
    self.number_of_free_forks = size
    self.replication_forks = list()
    self.just_unattached = dict()
    for i in range(size):
      self.replication_forks.append(ReplicationFork(genome=genome,speed=speed))
    for fork in self.replication_forks:
      self.just_unattached[fork] = False

#-----------------------------------------------------------------------------#

  ## This function checks if there is any fork (replication) colliding with
  # any RNAP (transcription) and handles the collision by rainsing the 
  # collision counter, changing the activation probability landscape around the
  # base affected and unattaching the affected fork.
  # @param time The simulation time when it was checked.
  # @param period The period of the RNAP carousel.
  # @param has_dormant Indication if the chromosome has dormant replication origins. 
  def check_replication_transcription_conflicts(self,time,period,has_dormant):

    number_of_collisions = 0
        
    # Current position of the RNAPs "carousel".
    # We assume that period < size of polycistronic region
    #
    RNAP_carousel_position = time % period

    for replication_fork in self.replication_forks:
      #
      # If it is not attached obviously there is no collision! :-)
      #
      if replication_fork.is_attached():

        chromosome = replication_fork.get_chromosome()

        for region in chromosome.transcription_regions:

          replisome_position_within_region = 0
          region_size = 0
          RNAP_direction = 0

          # Checks whether the current replication fork is within the current
          # transcription region; if it is, then it retrieves the RNAP
          # direction, otherwise it continues to the next iteration of the
          # inner loop.
          #
          if (region['start'] < region['end']):
            if replication_fork.get_base() < region['start']\
            or replication_fork.get_base() > region['end']:
              continue
            replisome_position_within_region =\
            replication_fork.get_base() - region['start']
            RNAP_direction = 1
          else:
            if replication_fork.get_base() < region['end']\
            or replication_fork.get_base() > region['start']:
              continue
            replisome_position_within_region =\
            region['start'] - replication_fork.get_base()
            RNAP_direction = -1

          # If this condition is true, then we have a head-to-head collision!
          #
          if replisome_position_within_region % period==RNAP_carousel_position\
            and replication_fork.get_direction() != RNAP_direction:

            # For debug purposes.
            #
            #if (region['start'] < region['end']):
            #  print('+ Replisome position: '+str(replication_fork.get_base()))
            #  print('+ RNAP position: ' + str(region['start']) + ' + '\
            #  + str(RNAP_carousel_position) + ' + ' + str(period) + ' x')
            #  print('+ End position: ' + str(region['end']) + '\n')
            #else:
            #  print('- Replisome position: '+str(replication_fork.get_base()))
            #  print('- RNAP position: ' + str(region['start']) + ' - '\
            #  + str(RNAP_carousel_position) + ' - ' + str(period) + ' x')
            #  print('- End position: ' + str(region['end']) + '\n')
                     
            if (has_dormant == True):
              chromosome.set_dormant_origin_activation_probability \
              (replication_fork.get_base())

            replication_fork.unattach()
            self.number_of_free_forks += 1
            self.just_unattached[replication_fork] = False
            number_of_collisions += 1
            
            # If there was a collision with this fork, then we do not need
            # to inspect the remaining regions with the current fork, hence we
            # can break the inner loop and evaluate the next fork.
            #
            break

    return number_of_collisions

#-----------------------------------------------------------------------------#

  ## This function moves all forks that are attached and prepares forks just
  # unattached that were not treated and makes the available as free forks.
  # @param time The time in the simulation when the forks were advanced.
  def advance_attached_forks(self, time):
    for fork in self.replication_forks:
      if self.just_unattached[fork]:
        self.just_unattached[fork] = False
        self.number_of_free_forks += 1

      if fork.is_attached():
        if not fork.advance(time=time):
          self.just_unattached[fork] = True

#-----------------------------------------------------------------------------#

  ## This function attaches available forks to a given genomic location. If
  # there are not enough forks, the just one or none is attached.
  # @param genomic_location The location where the fork will be attached.
  # @param time The simulation time when the attachment was done.
  # @see GenomicLocation
  def attach_forks(self, genomic_location, time):
    number_of_forks_attached_to_this_location = 0
    direction = 1
    
    for fork in self.replication_forks:
      if not fork.is_attached() and not self.just_unattached[fork]:
        fork.attach(genomic_location=genomic_location,\
        direction=direction, time=time)
        number_of_forks_attached_to_this_location += 1
        direction = - direction
        if number_of_forks_attached_to_this_location == 2:
          break

    self.number_of_free_forks -= number_of_forks_attached_to_this_location

#-----------------------------------------------------------------------------#

