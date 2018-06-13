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



## @package ReDyMo.src.chromosome
# Contains the class Chromosome.


## This class represents a Chromosome.
# 
# It stores relevant data about a Chromosome, such as lenght, number of
# replicated bases and has methods to query and modify the Chromosome.
class Chromosome:

    ## @var int number_of_replicated_bases
    # Stores the number os bases already replicated in that Chromosome.
    
    ## @var int number_of_origins
    # Number of replication origins available for the Chromosome.

    ## @var vector strand
    # Stores the time when each base was replicated. TODO:

    ## The constructor for a Chromosome object.
    # @param code The id of the Chromosome. TODO:
    # @param lenght The lenght of the chromosome
    # @param probabiliy_landscape The probability of each base to be an \
    # activation point
    # @param transcription_regions Still dont know what it does TODO:
    def __init__(self, code, length, probability_landscape,\
                 transcription_regions):
        self.code = code
        self.length = length
        self.strand = [0] * self.length
        self.activation_probabilities = probability_landscape
        self.number_of_replicated_bases = 0
        self.number_of_origins = 0
        self.transcription_regions = transcription_regions

#-----------------------------------------------------------------------------#

    ## Query the lenght of the Chromosome.
    # @return The lenght of the Chromosome.
    
    def __len__(self):
      return self.length

#-----------------------------------------------------------------------------#

    ## Print method for better visualization.
    # @return A string representation of the chromosome state.
    def __str__(self):
        chromosome_string = ""
        for i in range(0, len(self.strand), 500):
            chromosome_string += "{}\n".format(str(self.strand[i]))

        return chromosome_string

#-----------------------------------------------------------------------------#

    ## 
    # @param int base The index of a base to check.
    # @return Ture if the given base was replicated.
    def base_is_replicated(self, base):
        return True if self.strand[base] else False

#-----------------------------------------------------------------------------#

    ## Query the activation probabilty of a base. 
    # @param int base The index of a base to check. Note that it starts at 0.
    # @return The probability of a dormant origin to attach to the given
    # base based on the probability_landscape. 
    # @see probability_landscape
    def activation_probability(self, base):
        return self.activation_probabilities[base]

#-----------------------------------------------------------------------------#

    ## This method changes the probability landscape around the location of a
    # head-to-head collision. It sets the probability landscape with a Gaussian
    # function centered on the collision location, with parameters (a,b,c):
    # height of the mean (a) = 1, mean (b) = 0 and deviation (c) = 10000 bp.
    #
    # Therefore, the parameterized Gaussian function is defined as:
    #
    #                                     f(x) = a e^(-(x - b)^2 / (2 c^2))
    #                                          = 1 e^(-(x - 0)^2 / (2 10000^2))
    #                                          =   e^(-(x^2 / (2 10^8)).
    #
    # @param int base The index of the base around which the
    # probability_landscape will be changed. Note that it starts at 0.
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
            Gaussian_function_of_x = math.exp(- pow(x, 2) / (2 * pow(c, 2)))
            #
            # For debug purposes.
            #
            # print('x = ' + str(x) + ', f(x) = ' +\
            # str(Gaussian_function_of_x) + ', current probability = ' +\
            # str(self.activation_probabilities[current_base])   + '\n')
            #
            self.activation_probabilities[current_base] +=\
                                                        Gaussian_function_of_x
            if self.activation_probabilities[current_base] > 1:
                self.activation_probabilities[current_base] = 1

#-----------------------------------------------------------------------------#

    ## This function replicates the genome inside a given interval of bases.
    # This sets all the bases in the interval as replicated, and increasing
    # the number of replicated bases. 
    # @see number_of_replicated_bases.
    # @param int start The index of the first base to replicate.
    # @param int end The index of the last base to replicate.
    # @param float time The time wher the treplication ocurre, I think. TODO:
    # @retiurn true if was a normal (non reverse) transcription.
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

        for i in range(start, end + int(math.copysign(1, end - start)),
                       int(math.copysign(1, end - start))):

            if not self.strand[i]:
                self.strand[i] = time
                self.number_of_replicated_bases += 1

            elif i != start:               # The start position is always duplicated!
                is_normal_transcription = False
                break

        return is_normal_transcription

#-----------------------------------------------------------------------------#

    ## Checks if the entire Cromosome is replicated.
    # @return True if all bases have been replicated.
    # @see base_is_replicated
    # @see replicate
    def is_replicated(self):
        return self.number_of_replicated_bases == len(self)

#-----------------------------------------------------------------------------#

    ## Query the id of the Chromosome.
    # @return The code of the Chromosome.
    def get_code(self):
        return self.code

#-----------------------------------------------------------------------------#
