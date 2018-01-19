""" This file is part of ReDyMo.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>. """


class TranscriptionFork:
    """ Class managing each transcription machinery. """

    def __init__(self, speed, direction, end, base):
        self.end = end
        self.speed = speed
        self.direction = direction

        self.base = base
        self.is_spawn_duplicated = None
        # is the base in which this fork was attached duplicated? important for checking future collisions

    def is_outside_boundaries(self, base):
        return not base * self.direction <= self.end * self.direction
