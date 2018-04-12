#!/bin/bash

# With a very big timout (== 100000000!), to allow full replication.
#
time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 10 11 1 --speed 1 2 1 --period 0 --timout 100000000 --cells 10 1> out_10_0 2> err_10_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 10 11 1 --speed 1 2 1 --period 30 --timout 100000000 --cells 10 1> out_10_30 2> err_10_30

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 10 11 1 --speed 1 2 1 --period 90 --timout 100000000 --cells 10 1> out_10_90 2> err_10_90

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 10 11 1 --speed 1 2 1 --period 150 --timout 100000000 --cells 10 1> out_10_150 2> err_10_150

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 50 51 1 --speed 1 2 1 --period 0 --timout 100000000 --cells 10 1> out_50_0 2> err_50_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 50 51 1 --speed 1 2 1 --period 30 --timout 100000000 --cells 10 1> out_50_30 2> err_50_30

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 50 51 1 --speed 1 2 1 --period 90 --timout 100000000 --cells 10 1> out_50_90 2> err_50_90

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant True --resources 50 51 1 --speed 1 2 1 --period 150 --timout 100000000 --cells 10 1> out_50_150 2> err_50_150

