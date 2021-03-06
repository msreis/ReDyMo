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

from random import Random

from ReDyMo.src.genomic_location import GenomicLocation

## @package ReDyMo.src.genome
# Contains the class Genome.


## This class represents a Genome.
# It stores a set of Chromosomes and has methods to manipulate, replicate and 
# verify a Genome.
class Genome:

  rng = Random()

  ## The constructor 
  def __init__(self, chromosomes):
    self.chromosomes = chromosomes
    self.genome_size = 0
    for chromosome in self.chromosomes:
      self.genome_size += len(chromosome)

#-----------------------------------------------------------------------------#

  def __len__(self):
    length = 0
    for chromosome in self.chromosomes:
      length += len(chromosome)
    return length

#-----------------------------------------------------------------------------#

  def __iter__(self):
    return iter(self.chromosomes)

#-----------------------------------------------------------------------------#

  ## This function chooses a random base from a random Chromosome.
  # It does this using random integers from an uniform distribution.
  # @return A GenomicLocation object referencing the random base selected.
  # @see GenomicLocation
  def random_genomic_location(self):
    
    random_position = self.rng.randint(1, self.genome_size)    
    i = 0
    current_size = len(self.chromosomes[i])
    while random_position > current_size:
      i += 1
      current_size += len(self.chromosomes[i])
     
    random_base = self.rng.randint(0, len(self.chromosomes[i]) - 1)

    return GenomicLocation(base=random_base, chromosome=self.chromosomes[i])

#-----------------------------------------------------------------------------#

  ## This function chooses a random UNREPLICATED base from a random Chromosome.
  # It assumes that the genome is not completely replicated yet.
  # It does this using random integers from an uniform distribution.
  # @return A GenomicLocation object referencing the random base selected.
  # @see GenomicLocation
  def random_unreplicated_genomic_location(self):
    while 1:
      random_chromosome = self.chromosomes[self.rng.randint(0,\
                                           len(self.chromosomes) - 1)]
      random_base = self.rng.randint(0, len(random_chromosome) - 1)
      if not GenomicLocation(base=random_base,\
                             chromosome=random_chromosome).is_replicated():
        return GenomicLocation(base=random_base, chromosome=random_chromosome)

#-----------------------------------------------------------------------------#

  ## Checks if the Genome is entirely replicated.
  # It checks if all Chromosomes are completely replicated.
  # @return True if all bases of all Chromosomes have been replicated.
  # @see Chromosome
  def is_replicated(self):
    return all([chromosome.is_replicated() for chromosome in self.chromosomes])

#-----------------------------------------------------------------------------#

  ## This function calculates the average inter-origin distance across all
  # Chromosomes in the Genome.
  # @return The average inter-origin distance measured in number of bases.
  def average_interorigin_distance(self):
    number_of_interorigin_distances = 0
    for chromosome in self.chromosomes:
     #
     # There are three ways to compute IOD:
     #
     # a) IOD = len(chromosome) / number_of_origins
     #
     # b) IOD = len(chromosome) / number_of_origins - 1
     #
     # c) IOD = len(chromosome) / number_of_origins + 1
     #
     # (a) should be used in circular chromosomes, or in linear chromosomes
     # with a set of origin locations that minimizes the required replication
     # time.
     #
     # (b) should be used under the assumption that there are origins at
     # both subtelomeric regions (i.e., the extremities of the genome).
     #
     # (c) should be used in linear chromosome without the assumption of
     # of optimal origin positioning; therefore, IOD represents the homogeneous
     # partition of the chromosome by the set of origins.
     #
     number_of_interorigin_distances += chromosome.number_of_origins + 1

    return float(len(self)/number_of_interorigin_distances)

#-----------------------------------------------------------------------------#

  ## Retrieve the number of constitutive origins in the whole genome.
  # @return The number of constitutive origins in the whole genome.
  def number_of_constitutive_origins(self):
    n = 0
    for chromosome in self.chromosomes:
      n += chromosome.number_of_constitutive_origins()
    return n

#-----------------------------------------------------------------------------#
