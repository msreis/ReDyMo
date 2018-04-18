#!/bin/bash

# First computational assay in da Silva et al. (2018), manuscript submitted
# for publication in Nucleic Acids Research (NAR).

# These command lines were used to generate data depicted in Supplementary
# Table S1.

# The simulations were carried out with a very big timout (== 100000000!),
# in order to allow full replication.

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_10_0 2> err_10_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 20 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_20_0 2> err_20_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 30 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_30_0 2> err_30_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 40 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_40_0 2> err_40_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_50_0 2> err_50_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 60 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_60_0 2> err_60_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 70 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_70_0 2> err_70_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 80 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_80_0 2> err_80_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 90 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_90_0 2> err_90_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 100 --speed 1 --period 0 --timout 100000000 --cells 1000 1> out_100_0 2> err_100_0

