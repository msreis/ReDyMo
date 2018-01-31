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

from source.transcription_fork import TranscriptionFork


class TranscriptionRegion:
    """ Responsible for storing the transcription boundaries and guaranteeing the transcription frequency (period). """

    def __init__(self, start, end, period, speed):
        self.start = start - 1
        self.end = end - 1
        self.direction = int((end - start)/abs(end - start))
        self.period = period
        self.timer = 0.0
        self.transcription_speed = speed

    def spawn_fork(self, interval):
        if self.timer > self.period:
            self.timer = 0.0
            return(TranscriptionFork(speed=self.transcription_speed,
                                     direction=self.direction,
                                     end=self.end,
                                     base=self.start))
        else:
            if self.period < 0:
                self.timer += interval

            return None
