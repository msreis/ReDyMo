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
import random

from source.replication_fork import ReplicationFork


class Chromosome:
    def __init__(self, code, length, probability_landscape, transcription_regions):
        self.code = code
        self.length = length
        self.replication_speed = replication_speed
        self.genome = None

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
        """ Print method for better visualization. """

        replications = []
        bases = []
        transcriptions = []
        for i in range(len(self)):
            bases.append("-" if not self.strand[i] else "*")
            replications.append("R" if self.replication_forks.get(i) is not None else "-")
            transcriptions.append("-")

        for t in self.transcription_forks:
            transcriptions[t.base] = "T"

        chromosome_string = ""
        for i in range(len(self)):
            chromosome_string += "{} ".format(bases[i])
        chromosome_string += "\n"
        for i in range(len(self)):
            chromosome_string += "{} ".format(replications[i])
        chromosome_string += "\n"
        for i in range(len(self)):
            chromosome_string += "{} ".format(transcriptions[i])
        chromosome_string += "\n"

        return ""

    def conflict_status(self):
        """ Print method for output. """

        output_string = ""
        for i in self.conflict_bases:
            output_string += "{}\n".format(i)


    # This method changes the probability landscape around the location of a
    # head-to-head collision. It sets the probability landscape with a Gaussian
    # function centered on the collision location, with parameters (a,b,c):
    # height of the mean (a) = 1, mean (b) = 0 and deviation (c) = 10000 bp.
    #
    # Therefore, the parameterized Gaussian function is defined as: 
    #
    #                                      f(x) = a e^(-(x - b)^2 / (2 c^2))
    #                                           = 1 e^(-(x - 0)^2 / (2 10000^2))
    #                                           =   e^(-(x^2 / (2 10^8)).
    #
    def set_dormant_origin_activation_probability(self, base):
      c = 10000
      leftmost_base = base - 2 * c    # 2 deviations left
      if leftmost_base < 0:
        leftmost_base = 0
      rightmost_base = base + 2 * c   # 2 deviations right
      if rightmost_base >= self.length:
        rightmost_base = self.length - 1
      for current_base in range(leftmost_base, rightmost_base):
        x = current_base - base
        Gaussian_function_of_x = math.exp(- pow(x,2) / (2 * pow(c,2)) )
        #
        # For debug purposes.
        #
        # print('x = ' + str(x) + ', f(x) = ' + str(Gaussian_function_of_x) + ', current probability = ' + str(self.activation_probabilities[current_base])   + '\n')
        self.activation_probabilities[current_base] += Gaussian_function_of_x
        if self.activation_probabilities[current_base] > 1:
          self.activation_probabilities[current_base] = 1

    def replicate(self, start, end, time):
        if start == end:
            self.number_of_origins += 1

    def advance_transcriptions(self, interval):
        """ Advance the transcription machineries AND deal with collisions with replication machineries. """

        freed_forks = 0
        for index, transcription in enumerate(self.transcription_forks):
            final_base = None
            for i in range(transcription.base,
                           transcription.base + transcription.speed * transcription.direction * interval,
                           transcription.direction):
                if transcription.is_outside_boundaries(base=i):
                    self.transcription_forks.pop(index)
                    break

                if transcription.is_spawn_duplicated != self.is_base_replicated(base=i):
                    self.transcription_forks.pop(index)
                    if self.is_base_replicated(base=i):
                        for j in range(i, i - (self.replication_speed * interval + 2) * transcription.direction,
                                       - transcription.direction):
                            if self.replication_forks.get(j) is not None:
                                self.replication_forks.pop(j)
                                self.conflict_bases.append(j)
                                freed_forks += 1
                                break

                    break

                final_base = i

            transcription.base = final_base

        return freed_forks

    def advance_replications(self, interval, time):
        """ Advance replication machineries until they reach a replicated region or an end of the chromosome. """

        freed_forks = 0
        for base, fork in self.replication_forks.items():
            final_base = None
            conflict = False

            for i in range(base,
                           base + fork.speed * fork.direction * interval,
                           fork.direction):
                final_base = i

                if i < 0 or i > len(self) - 1 or self.is_base_replicated(i):
                    conflict = True
                    break

            self.replicate(start=base, end=final_base, time=time)
            if conflict:
                final_base = None
                freed_forks += 1

            fork.base = final_base

        new_dict = dict()
        for base, fork in self.replication_forks.items():
            if fork.base is not None:
                new_dict[fork.base] = fork

        self.replication_forks = new_dict

        return freed_forks

    def is_base_replicated(self, base):
        """ Tests whether this base was replicated. """

        return bool(self.strand[base])

    def replicate(self, start, end, time):
        """ Modify the DNA strand's bases between start and end from non-replicated to replicated. """

        direction = int(math.copysign(1, end - start))
        for i in range(start, end, direction):
            if not self.strand[i]:
                self.strand[i] = time
                self.number_of_replicated_bases += 1

    def is_replicated(self):
        """ Tests whether this chromosome is fully replicated. """

        return self.number_of_replicated_bases == len(self)


    def get_code(self):
        return self.code


