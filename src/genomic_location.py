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

import random


## @package ReDyMo.src.genomic_location
# Contains the class GenomicLocation.


## This class represents a base from a chromosome called a Genomic Location.
# It stores a set of Chromosomes and has methods to check and query a base 
# from a Genome.
class GenomicLocation:

  ## The constructor.
  # @param int base The index of the base that this location represents.
  # @param Chromosome chromosome The Chromosome which contains the given base.
  # @see Chromosome
  def __init__(self, base, chromosome):
    self.base = base
    self.chromosome = chromosome

#-----------------------------------------------------------------------------#

  ## Queries if the particular base has been replicated.
  # @return True if the base is replicated.
  def is_replicated(self):
    return self.chromosome.base_is_replicated(base=self.base)

#-----------------------------------------------------------------------------#

  ## Tests the probability of the base to be activated
  # @return True if the base will be activated
  def will_activate(self):
    return random.random() < self.chromosome.activation_probability\
    (base=self.base)

#-----------------------------------------------------------------------------#

