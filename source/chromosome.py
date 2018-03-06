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

import math


class Chromosome:
    def __init__(self, code, length, probability_landscape, transcription_regions):
        self.code = code
        self.length = length
        self.strand = [0] * self.length
        self.activation_probabilities = probability_landscape
        self.number_of_replicated_bases = 0
        self.number_of_origins = 0
        self.transcription_regions = transcription_regions

    def __len__(self):
        return self.length

    # Print method for better visualization.
    #
    def __str__(self):
        chromosome_string = ""
        for i in range(0, len(self.strand), 500):
            chromosome_string += "{}\n".format(str(self.strand[i]))

        return chromosome_string

    def base_is_replicated(self, base):
        return True if self.strand[base] else False

    def activation_probability(self, base):
        return self.activation_probabilities[base]

    def replicate(self, start, end, time):
        if start == end:
            self.number_of_origins += 1

        is_normal_transcription = True
        if end < 0:
            is_normal_transcription = False
            end = 0

        elif end > len(self) - 1:
            is_normal_transcription = False
            end = len(self) - 1

        for i in range(start, end + int(math.copysign(1, end - start)), int(math.copysign(1, end - start))):
            if not self.strand[i]:
                self.strand[i] = time
                self.number_of_replicated_bases += 1

            elif i != start:    # The start position is always duplicated
                is_normal_transcription = False
                break

        return is_normal_transcription

    def is_replicated(self):
        return self.number_of_replicated_bases == len(self)


    def get_code(self):
        return self.code


