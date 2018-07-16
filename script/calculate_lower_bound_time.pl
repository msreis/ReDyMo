#!/usr/bin/perl -w

# This file is part of ReDyMo.
#
#    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.
#
#    ReDyMo is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the
#    Free Software Foundation, either version 3 of the License, or (at your
#    option) any later version.
#    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#    for more details.
#    You should have received a copy of the GNU General Public License along
#    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.
#
#

# This program calculates an returns the lower-bound time of DNA replication
# of a chromosome given:
#
# 1) Replisome speed (v);
#
# 2) Chromosome size (N);
#
# 3) Set of putative constitutive origin locations (Theta).
#
# To this end, this program implements the formula presented in Equation 4 of
# da Silva et al. (2018).

use strict;

@ARGV == 3 or die
  "\nSyntax: $0 replisome-speed chromosome-size chromosome-number\n\n";

my $v = $ARGV[0];

my $N = $ARGV[1];

my $j = $ARGV[2];

# First, we define the set of putative constitutive origins (Theta); these
# values are for T. brucei TREU927 and were extracted from MFA-seq data 
# presented in Figure 4 of Tiengwe et al. (2012).
#
my @Theta = ([],
  [686746, 807228],                                                      # Chr01
  [301204, 409638, 1036144],                                             # Chr02
  [879518, 981927, 1228915],                                             # Chr03
  [319277, 945783, 1283132],                                             # Chr04
  [186746, 686746, 1331325],                                             # Chr05
  [24096, 1277108],                                                      # Chr06
  [240963, 1975903],                                                     # Chr07
  [469879, 861445, 1174698, 1451807, 1891566, 2240963],                  # Chr08
  [644578, 1150602, 1716867, 2234939],                                   # Chr09
  [801200, 1234939, 1626506, 1927710, 2361445, 2638554],                 # Chr10
  [180722, 542168, 1355421, 1873493, 2192771, 2602409, 2903614, 3463855] # Chr11
            );


# Now, we compute Equation 4 with the obtained v, N and Theta_j.
#
my $T = 0;


# These two lines include a pair of origins, each one located 10 Kbp from 
# each chromosome extremity. The assumption here is that all subtelomeric
# regions contain a replication origin. 
#
#unshift @{$Theta[$j]}, 10000;
#push @{$Theta[$j]}, $N - 10000;


foreach my $i (0..(scalar @{$Theta[$j]}))
{
  my $monomial;

  if ($i == 0)
  {
    $monomial = $Theta[$j]->[$i] / $v;
  }
  elsif ($i == scalar @{$Theta[$j]})
  {
    $monomial = ($N - $Theta[$j]->[$i-1]) / $v;
  }
  else
  {
    $monomial = ($Theta[$j]->[$i] - $Theta[$j]->[$i-1]) / (2 * $v);
  }

  if ($monomial > $T)
  {
    $T = $monomial;
  }
}

printf "Chr%d, v = $v bp/sec: T(Theta,<1,N>) = %6.2f sec.\n", $j,$T;

# End of program.
#
exit 0;
