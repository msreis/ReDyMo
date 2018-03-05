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

    def __init__(self, start, end):
        self.base = start
        self.end = end
        self.direction = int((end - start)/abs(end - start))  # Either -1 or +1.
 
    def advance(self):
        base = self.base + self.direction
        if self.direction == 1 and base == (end + 1):
           return False
        if self.direction == -1 and base == (end - 1):
           return False
        return True

    def position(self):
        return base
