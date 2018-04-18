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

class ReplicationFork:
    def __init__(self, genome, speed):
        self.genome = genome
        self.speed = speed

        self.base = None
        self.chromosome = None
        self.direction = None

    def attach(self, genomic_location, direction, time):
        if self.is_attached():
            raise ValueError("Tried to attach an already attached fork")

        self.base = genomic_location.base
        self.chromosome = genomic_location.chromosome
        self.direction = direction

        self.chromosome.replicate(start=self.base,
                                  end=self.base,
                                  time=time)

    def get_direction(self):
        return self.direction


    def get_base(self):
        return self.base


    def get_chromosome(self):
        return self.chromosome


    def unattach(self):
        self.base = None
        self.chromosome = None
        self.direction = None

    def advance(self, time):
        new_base = self.base + self.speed * self.direction

        if not self.chromosome.replicate(start=self.base,
                                         end=new_base,
                                         time=time):
            self.unattach()
            return False

        self.base = new_base
        return True

    def is_attached(self):
        return self.base is not None


