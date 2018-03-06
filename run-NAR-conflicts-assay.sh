#!/bin/bash

# With timeout == 1.25 of mean S-phase duration in the no-transcripton assay
#
time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 0 --timout 3505120 --cells 10 1> out_10_0 2> err_10_0 &
mv output output_10_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 30 --timout 3505120 --cells 10 1> out_10_30 2> err_10_30 &
mv output output_10_30

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 90 --timout 3505120 --cells 10 1> out_10_90 2> err_10_90 &
mv output output_10_90

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 150 --timout 3505120 --cells 10 1> out_10_150 2> err_10_150 &
mv output output_10_150

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 11 1 --speed 1 2 1 --period 0 --timout 3505120 --cells 10 1> out_50_0 2> err_50_0 &
mv output output_50_0

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 30 --timout 679358 --cells 10 1> out_50_30 2> err_50_30 &
mv output output_50_30

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 90 --timout 679358 --cells 10 1> out_50_90 2> err_50_90 &
mv output output_50_90

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 150 --timout 679358 --cells 10 1> out_50_150 2> err_50_150 &
mv output output_50_150

# With very large timeout (100 million iterations!)
#
time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 150 --timout 100000000 --cells 10 1> out_10_150_inf 2> err_10_150_inf &
mv output output_10_150_inf

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 90 --timout 100000000 --cells 10 1> out_10_90_inf 2> err_10_90_inf &
mv output output_10_90_inf

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 1 2 1 --period 30 --timout 100000000 --cells 10 1> out_10_30_inf 2> err_10_30_inf &
mv output output_10_30_inf

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 150 --timout 100000000 --cells 10 1> out_50_150_inf 2> err_50_150_inf &
mv output output_50_150_inf

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 90 --timout 100000000 --cells 10 1> out_50_90_inf 2> err_50_90_inf &
mv output output_50_90_inf

time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 50 51 1 --speed 1 2 1 --period 30 --timout 100000000 --cells 10 1> out_50_30_inf 2> err_50_30_inf &
mv output output_50_30_inf

