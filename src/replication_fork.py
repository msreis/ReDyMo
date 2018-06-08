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

## @package ReDyMo.src.replication_fork
# Contains the class ReplicationFork.


## This class replresents a replication fork.
# 
class ReplicationFork:

  ## The constructor.
  # @param Genome genome The Genome to which this fork belongs to.
  # @param int speed The speed, in bases per step, at which the
  # fork replicates.
  def __init__(self, genome, speed):
    self.genome = genome
    self.speed = speed
    self.base = None
    self.chromosome = None
    self.direction = None

#-----------------------------------------------------------------------------#
  ## This function assigns the fork to a given base and chromosome
  # (genomic location) and replicates this base right away.
  # @param GenomicLocation genomic_location This is the position to which the
  # fork will attach.
  # @param int direction The direction to which the fork should move
  # (left or right) in a Chromosome.
  # @param int time The time when this attachment ocuurs in the simulation.
  def attach(self, genomic_location, direction, time):

    if self.is_attached():
      raise ValueError("Tried to attach an already attached fork")

    self.base = genomic_location.base
    self.chromosome = genomic_location.chromosome
    self.direction = direction

    self.chromosome.replicate(start = self.base,
                                end = self.base,
                               time = time)

#-----------------------------------------------------------------------------#
  ## Direction attribute getter.
  def get_direction(self):
    return self.direction

#-----------------------------------------------------------------------------#
  ## Base attribute getter.
  def get_base(self):
    return self.base

#-----------------------------------------------------------------------------#

  ## Chromosome attribute getter.
  def get_chromosome(self):
    return self.chromosome

#-----------------------------------------------------------------------------#
  ## Unbinds the fork from the position where it was.
  def unattach(self):
    self.base = None
    self.chromosome = None
    self.direction = None

#-----------------------------------------------------------------------------#

  ## Advances the fork proportionally to its speed and replicates the bases in
  # the path.
  # @param int time The time of the dimluation when these base replications
  # happen.
  # @return True if the replication went well.
  def advance(self, time):
    new_base = self.base + self.speed * self.direction

    if not self.chromosome.replicate(start=self.base, end=new_base, time=time):
      self.unattach()
      return False

    self.base = new_base
    return True

#-----------------------------------------------------------------------------#
  ## This function queries the attachment status of the fork.
  # @return True if the fork is attached to some base in any chromosome.
  def is_attached(self):
    return self.base is not None

#-----------------------------------------------------------------------------#

