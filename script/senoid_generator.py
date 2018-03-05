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

import sys
from math import sin, pi

n = float(sys.argv[2])/(2 * 64 * 8312)
k = (2 * pi * n)/1000
with open(sys.argv[1], 'w') as output_file:
    for i in range(0, 1001):
        value = max(10000 * sin(k * i + 1000/(4 * n)), 1)
        output_file.write("{}\n".format(value))

