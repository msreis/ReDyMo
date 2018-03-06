""" This file is part of ReDyMo.

    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.
    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ortra
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.
    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.

"""

from source.replication_fork import ReplicationFork

from source.transcription_fork import TranscriptionFork

from array import *


class ForkManager:

    def __init__(self, size, genome, speed):
        self.replication_forks = list()
        for i in range(size):
            self.replication_forks.append(ReplicationFork(genome=genome, speed=speed))
        self.just_unattached = dict()
        for fork in self.replication_forks:
            self.just_unattached[fork] = False
        self.number_of_free_forks = size

        # Transcription arrays initialization.
        self.transcription_array = dict()
        for chromosome in genome.chromosomes:
          self.transcription_array[chromosome] = array('b', (0 for x in range(0, len(chromosome))))

        # List of active transcriptions initialization.
        self.transcription_forks = list()

    def spawn_transcription_forks(self, genome):
        # For each chromosome, iterates over each of its polycistronic regions.
        for chromosome in genome.chromosomes:
            for region in chromosome.transcription_regions:
                  if (region['start'] < region['end']):
                       self.transcription_array[chromosome][region['start']] = 1
                  else:
                       self.transcription_array[chromosome][region['end']] = -1                   
                  self.transcription_forks.append(TranscriptionFork(start=region['start'], end=region['end'], chromosome=chromosome))


    def advance_transcription_forks(self):
        for transcription_fork in self.transcription_forks:
            if not transcription_fork.advance(transcription_array = self.transcription_array[transcription_fork.get_chromosome()]):
                   self.transcription_forks.remove(transcription_fork)


    def check_replication_transcription_conflicts(self):
        number_of_collisions = 0

        for replication_fork in self.replication_forks:
           #
           # If it is not attached obviously there is no collision! :-)
           #
           if replication_fork.is_attached():
             transcription_fork_direction = self.transcription_array[replication_fork.get_chromosome()][replication_fork.is_attached()]
             if  transcription_fork_direction != 0 \
             and transcription_fork_direction != 2 \
             and transcription_fork_direction != replication_fork.get_direction():
               #
               # We set a flag ('2') to indicate that this RNAP was removed; its respective transcription_fork object
               # will be removed during the next RNAPs advances.
               #
               self.transcription_array[replication_fork.get_chromosome()][replication_fork.is_attached()] = 2
               replication_fork.unattach()
               self.number_of_free_forks += 1 
               number_of_collisions += 1

        return number_of_collisions


    def advance_attached_forks(self, time):
        for fork in self.replication_forks:
            if self.just_unattached[fork]:
                self.just_unattached[fork] = False
                self.number_of_free_forks += 1

            if fork.is_attached():
                if not fork.advance(time=time):
                    self.just_unattached[fork] = True

    def attach_forks(self, genomic_location, time):
        number_of_forks_attached_to_this_location = 0
        direction = 1
        for fork in self.replication_forks:
            if not fork.is_attached() and not self.just_unattached[fork]:
                fork.attach(genomic_location=genomic_location, direction=direction, time=time)
                number_of_forks_attached_to_this_location += 1
                direction = - direction
                if number_of_forks_attached_to_this_location == 2:
                    break
        self.number_of_free_forks -= number_of_forks_attached_to_this_location

