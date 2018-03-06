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

class TranscriptionFork:
    """ Class managing each transcription machinery. """

    def __init__(self, start, end, chromosome):
        self.base = start
        self.end = end
        self.direction = int((end - start)/abs(end - start))  # Either -1 or +1.
        self.chromosome = chromosome 

    def advance(self, transcription_array):

        # If this RNAP was already removed due a replication-transcription 
        # conflict (which is indicated by the '2' flag), we proceed to remove
        # it completely from the transcription array and also from the
        # transcription_fork list.
        #
        if transcription_array[self.base] == 2:
           transcription_array[self.base] = 0
           return False

        # Update base in array.
        #
        transcription_array[self.base] = 0

        # Advance RNAP and check if transcription is finished.
        #
        self.base = self.base + self.direction
        if self.direction == 1 and self.base == (self.end + 1):
           return False
        if self.direction == -1 and self.base == (self.end - 1):
           return False

        # If not, update base in array.
        #
        if self.direction == 1:
           transcription_array[self.base] = 1
        else:
           transcription_array[self.base] = -1
        return True

    def position(self):
        return self.base

    def get_chromosome(self):
        return self.chromosome

