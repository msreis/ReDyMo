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

  ## Tests the probability of the base to be activated.
  # @param Boolean use_constitutive_origins True if uses this type of origin.
  # @param int origins_range Considered range around a constitutive origin.
  # @return True if the base will be activated.
  def will_activate(self, use_constitutive_origins, origins_range):
  
    if (not use_constitutive_origins):  
      return random.random() < self.chromosome.activation_probability\
      (base=self.base)

    # We define a range of 'origins_range' upstream and downstream the
    # constitutive origin that can be activated, with the origin located at
    # the middle of such range.
    #
    for origin in self.chromosome.constitutive_origins:  
      if (self.base >= (origin - origins_range / 2))\
      and (self.base <= (origin + origins_range / 2))\
      and origin not in self.chromosome.fired_constitutive_origins:
        return True
  
    return False

#-----------------------------------------------------------------------------#

  ## Retrieve a constitutive origin located in this range.
  # @param int origins_range Considered range around a constitutive origin.
  # @return True if the base will be activate, False otherwise.
  def get_constitutive_origin(self, origins_range):
  
    # We define a range of 'origins_range' upstream and downstream the
    # constitutive origin that can be activated, with the origin located at
    # the middle of such range.
    #
    for origin in self.chromosome.constitutive_origins:  
      if (self.base >= (origin - origins_range / 2))\
      and (self.base <= (origin + origins_range / 2))\
      and origin not in self.chromosome.fired_constitutive_origins:
        return origin 
          
    return 0

#-----------------------------------------------------------------------------#

  ## Update the list of fired constitutive origins with an fired origin.
  # @param int location of the constitutive origin.
  # @return True if list was successfully updated and False otherwise.
  def put_fired_constitutive_origin(self, origin):
  
    for current_origin in self.chromosome.constitutive_origins:  

      if (current_origin == origin):
        # If 'origin' is already in the fired list, then it does nothing!
        if (current_origin in self.chromosome.fired_constitutive_origins):
          return False
        else:
          self.chromosome.fired_constitutive_origins.append(origin)
          return True

    # If it reaches here, 'origin' was not found in the original list of 
    # constitutive origins.
    #
    return False

#-----------------------------------------------------------------------------#

