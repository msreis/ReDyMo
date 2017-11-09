import sys
from math import sin, pi

n = float(sys.argv[2])/(2 * 64 * 8312)
k = (2 * pi * n)/1000
with open(sys.argv[1], 'w') as output_file:
    for i in range(0, 1001):
        value = max(10000 * sin(k * i + 1000/(4 * n)), 1)
        output_file.write("{}\n".format(value))

