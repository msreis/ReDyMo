#!/usr/bin/perl -w

# First computational assay in da Silva et al. (2018), manuscript submitted
# for publication in Nucleic Acids Research (NAR).


# The simulations were carried out with a very big timeout (== 100000000!),
# in order to allow full replication.
#
my $TIMEOUT = 100000000;

use strict;

my $NUMBER_OF_SIMULATIONS = 100; 

for (my $F = 10; $F <= 100; $F += 10)
{
  foreach my $period (0, 900, 750, 600, 450, 300, 150, 90)
  {
    system ("time python3 ./main.py --organism 'Trypanosoma brucei brucei TREU927' --dormant False --resources $F --speed 1 --period $period --timeout $TIMEOUT --cells $NUMBER_OF_SIMULATIONS 1> out_10_0 2> err_10_0");
  }
}

# End of program.
#
exit 0;

