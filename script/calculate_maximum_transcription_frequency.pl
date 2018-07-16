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

# This program calculates an returns the maximum allowed polycistronic 
# transcription frequency of a chromosome given:
#
# 1) Replisome speed (v);
#
# 2) Chromosome size (N);
#
# 3) Set of putative constitutive origin locations (Theta);
#
# 4) fasta file with CDS locations (Alpha and Beta).
#
# To this end, this program implements the formula presented in Equation 4 of
# da Silva et al. (2018).

use strict;

$| = 1;

@ARGV == 4 or die
  "\nSyntax: $0 replisome-speed chromosome-size chromosome-number CDS-file\n\n";

my $v = $ARGV[0];

my $N = $ARGV[1];

my $j = $ARGV[2];

my $CDS_file = $ARGV[3];


# Set this variable as 1 to enable a verbose debug mode.
#
my $DEBUG = 0;

# Set this variable as 1 to include two origins into subtelomeric regions.
#
my $SUBTELOMERIC_ORIGINS = 1;


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


# These two pushes include a pair of origins, each one located 10 Kbp from 
# each chromosome extremity. The assumption here is that all subtelomeric
# regions contain a replication origin. 
#
if ($SUBTELOMERIC_ORIGINS == 1)
{
  unshift @{$Theta[$j]}, 10000;
  push @{$Theta[$j]}, $N - 10000;
}

# Load CDS data.
#
my @regions;

open (INPUT, $CDS_file) or die "Could not open $CDS_file!\n";

my @chromosome;

$chromosome[$_] = 0 foreach 1..$N; # 0 == no CDS.

while (<INPUT>)
{
  if (($_ =~ /location\=Tb927_0?(\d+).*\:(\d+)\-(\d+)\((\S)\)/) && ($1 == $j))
  {
    for (my $i = $2; $i <= $3; $i++)
    {
      if ($4 eq '+')
      {
        $chromosome[$i] = 1;  # 1 == sense CDS.
      }    
      else
      {
        $chromosome[$i] = -1; # -1 == antisense CDS.
      }        
    }
  }
}
close (INPUT);

# Now, we compute Eq. 5 with the obtained v, N, Theta_j, Alpha_j, and Beta_j.
#
my $period = 0; # initial period == 0


foreach my $i (0..$#{$Theta[$j]})
{
  my $monomial;

  if ($i == 0)
  {
    $monomial = get_alpha ($Theta[$j]->[$i], $v, \@chromosome);
  }
  elsif ($i == $#{$Theta[$j]})
  {
    $monomial = get_beta ($Theta[$j]->[$i], $N, $v, \@chromosome);
  }
  else
  {
    $monomial = get_alpha_and_beta
                ($Theta[$j]->[$i-1], $Theta[$j]->[$i], $v, \@chromosome);
  }

  if ($monomial > $period)
  {
    $period = $monomial;
  }
}

if ($period == 0)
{
  printf "Chr%d, v = $v bp/sec: Freq(Theta,<1,N>,A,B) = 0.0000 mHz.\n", $j;
}
else
{
  printf "Chr%d, v = $v bp/sec: Freq(Theta,<1,N>,A,B) = %4.4f mHz.\n",
       $j, ($v / (2 * $period)) * 1000;
}

# End of program.
#
exit 0;


sub get_alpha
{
  my ($e, $v, $ref_chr) = @_;

  # For debug purposes, it prints the orientation of all CDSes in this strecht.
  # 0: no CDS; 1: sense CDS; -1: antisense CDS.
  #
  if ($DEBUG == 1)
  {
    print "In get\_alpha: ";
    my $current_CDS = 0;
    for (my $i = 1; $i <= $e; $i++)
    {
      if ($ref_chr->[$i] != $current_CDS)
      {
        print "$current_CDS ";
        $current_CDS = $ref_chr->[$i];
      }
    }
    print "\n";
  }

  my $max_period = 0;
  
  my $within_sense_CDS = 0;
  my $sense_period = 0;
  
  for (my $i = 1; $i <= $e; $i++)
  {
    if (($ref_chr->[$i] == 1) && ($within_sense_CDS == 0))
    {
      $within_sense_CDS = 1;
      $sense_period = 0;
    }
    elsif (($ref_chr->[$i] == 1) && ($within_sense_CDS == 1))
    {
      $sense_period++;    
    }
    elsif (($ref_chr->[$i] != 1) && ($within_sense_CDS == 1))
    {
      $within_sense_CDS = 0;
    }

    ($sense_period > $max_period) and $max_period = $sense_period;
  }

  return $max_period;
}


sub get_beta
{
  my ($s, $N, $v, $ref_chr) = @_;

  # For debug purposes, it prints the orientation of all CDSes in this strecht.
  # 0: no CDS; 1: sense CDS; -1: antisense CDS.
  #
  if ($DEBUG == 1)
  {
    print "In get\_beta: ";
    my $current_CDS = 0;
    for (my $i = $s; $i <= $N; $i++)
    {
      if ($ref_chr->[$i] != $current_CDS)
      {
        print "$current_CDS ";
        $current_CDS = $ref_chr->[$i];
      }
    }
    print "\n";    
  }

  my $max_period = 0;
  
  my $within_antisense_CDS = 0;
  my $antisense_period = 0;
  
  for (my $i = $s; $i <= $N; $i++)
  {
    if (($ref_chr->[$i] == -1) && ($within_antisense_CDS == 0))
    {
      $within_antisense_CDS = 1;
      $antisense_period = 0;
    }
    elsif (($ref_chr->[$i] == -1) && ($within_antisense_CDS == 1))
    {
      $antisense_period++;    
    }
    elsif (($ref_chr->[$i] != -1) && ($within_antisense_CDS == 1))
    {
      $within_antisense_CDS = 0;
    }

    ($antisense_period > $max_period) and $max_period = $antisense_period;
  }
  
  return $max_period;
}


sub get_alpha_and_beta
{
  my ($s, $e, $v, $ref_chr) = @_;
  
  # For debug purposes, it prints the orientation of all CDSes in this strecht.
  # 0: no CDS; 1: sense CDS; -1: antisense CDS.
  #
  if ($DEBUG == 1)
  {
    print "In get\_alpha\_and\_beta: ";
    my $current_CDS = 0;
    for (my $i = $s; $i <= $e; $i++)
    {
      if ($ref_chr->[$i] != $current_CDS)
      {
        print "$current_CDS ";
        $current_CDS = $ref_chr->[$i];
      }
    }
    print "\n";
  }
  
  my $max_period = 0;

  # Array to store the maximum sense period of a given position (B_i^j).
  #
  my @forward_stretch;
  $forward_stretch[$_] = 0 foreach 1..($e - $s + 1); 
  
  my $within_antisense_CDS = 0;
  my $antisense_period = 0;
  
  for (my $i = $s; $i <= $e; $i++)
  {
    if (($ref_chr->[$i] == -1) && ($within_antisense_CDS == 0))
    {
      $within_antisense_CDS = 1;
      $antisense_period = 0;
    }
    elsif (($ref_chr->[$i] == -1) && ($within_antisense_CDS == 1))
    {
      $antisense_period++;    
    }
    elsif (($ref_chr->[$i] != -1) && ($within_antisense_CDS == 1))
    {
      $within_antisense_CDS = 0;
    }

    ($antisense_period > $max_period) and $max_period = $antisense_period;

    $forward_stretch[$i - $s + 1] = $max_period; 
  }

  # Array to store the maximum antisense period of a given position (A_i^j).
  #
  my @backward_stretch;
  $backward_stretch[$_] = 0 foreach 1..($e - $s + 1); 
  
  my $within_sense_CDS = 0;
  my $sense_period = 0;
  
  $max_period = 0;
  
  for (my $i = $e; $i >= $s; $i--)
  {
    if (($ref_chr->[$i] == 1) && ($within_sense_CDS == 0))
    {
      $within_sense_CDS = 1;
      $sense_period = 0;
    }
    elsif (($ref_chr->[$i] == 1) && ($within_sense_CDS == 1))
    {
      $sense_period++;    
    }
    elsif (($ref_chr->[$i] != 1) && ($within_sense_CDS == 1))
    {
      $within_sense_CDS = 0;
    }

    ($sense_period > $max_period) and $max_period = $sense_period;

    $backward_stretch[$i - $s + 1] = $max_period; 
  }
  
  $max_period = 0;

  my $min_period = $e - $s + 2;

  # Finally, we minimize the maximum between two elements of the two arrays 
  # such that these two elements have the same index.
  #
  for (my $i = $s; $i <= $e; $i++)
  {
    # Maximin problem.
    #
    my $current_minimum = $backward_stretch[$i - $s + 1];    
    ($forward_stretch[$i - $s + 1] < $current_minimum)
      and $current_minimum = $forward_stretch[$i - $s + 1];
    ($current_minimum > $max_period) and $max_period = $current_minimum;

    # The equivalent minimax problem.
    #
    my $current_maximum = $backward_stretch[$i - $s + 1];
    ($forward_stretch[$i - $s + 1] > $current_minimum)
      and $current_maximum = $forward_stretch[$i - $s + 1];
    ($current_maximum < $min_period) and $min_period = $current_maximum;
  }
  
  if ($min_period != $max_period)
  {
    print "Error! Minimax solution is different of the maximin one!\n";
  }

  return $min_period;
}


