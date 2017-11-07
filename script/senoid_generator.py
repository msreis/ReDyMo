from math import sin, pi
import sys


n = float(sys.argv[2])/(2 * 64 * 8312)
k = (2 * pi * n)/1000
with open(sys.argv[1], 'w') as output_file:
    for i in range(0, 1001):
        value = max(sin(k * i + 1000/(4 * n)), 0)
        output_file.write("{}\n".format(value))
