#!/bin/bash

# Third computational assay in da Silva et al. (2018), manuscript submitted
# for publication in Nucleic Acids Research (NAR).

# These command lines were used to generate data depicted in Supplementary
# Tables S2 and S3.

# The simulations were carried out with a very big timout (== 100000000!),
# in order to allow full replication.

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 0 --timout 100000000 --cells 10 1> out_10_0 2> err_10_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 900 --timout 100000000 --cells 10 1> out_10_900 2> err_10_900

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 750 --timout 100000000 --cells 10 1> out_10_750 2> err_10_750

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 600 --timout 100000000 --cells 10 1> out_10_600 2> err_10_600

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 450 --timout 100000000 --cells 10 1> out_10_450 2> err_10_450

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 300 --timout 100000000 --cells 10 1> out_10_300 2> err_10_300

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 10 --speed 1 --period 150 --timout 100000000 --cells 10 1> out_10_150 2> err_10_150



time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 0 --timout 100000000 --cells 10 1> out_50_0 2> err_50_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 900 --timout 100000000 --cells 10 1> out_50_900 2> err_10_900

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 750 --timout 100000000 --cells 10 1> out_50_750 2> err_10_750

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 600 --timout 100000000 --cells 10 1> out_50_600 2> err_10_600

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 450 --timout 100000000 --cells 10 1> out_50_450 2> err_10_450

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 300 --timout 100000000 --cells 10 1> out_50_300 2> err_10_300

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources 50 --speed 1 --period 150 --timout 100000000 --cells 10 1> out_50_150 2> err_50_150

