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

# This program receives a TriTrypDB genome fasta and prints into STDOUT the
# global AT content of each chromosome, one chromosome per line.
#
# Syntax examples:
#
# ./$0 ../data/TriTrypDB-34_TbruceiTREU927_Genome.fasta
#
# ./$0 ../data/TriTrypDB-34_TbruceiLister427_Genome.fasta
#
# M.S.Reis, December 19, 2017.

use strict;

my $NUMBER_OF_CHROMOSOMES = 11;

my $WINDOW = 1000;


my (@chromosome, @AT_content);


# Read the chromosomes.
#
my $chr = 0;

@ARGV == 1 or die "\nSyntax: ./$0 genome-fasta-file-and-path\n\n";

open IN, $ARGV[0] or die "Error opening '" . $ARGV[0] . "' file!\n";

while ($chr <= $NUMBER_OF_CHROMOSOMES)
{
  $_ = <IN>;
  chomp $_;
  if ($_ =~ /^\>(\S+)*/)
  {
    $chr++;
    $chromosome[$chr] = "";
  }
  else
  {
    $chromosome[$chr] .= $_;
  }
}

close IN;

# First we screen a window throughout each chromosome.
#
foreach my $i (1..$NUMBER_OF_CHROMOSOMES)
{
  for (my $j = 0; $j < length $chromosome[$i]; $j = $j + $WINDOW)
  {
    my $AT = 0;

    my $current_window = $WINDOW;

    if (((length $chromosome[$i]) - $j) < $WINDOW)
    {
      $current_window = (length $chromosome[$i]) - $j;
    }

    for (my $k = 0; $k < $current_window; $k++)
    {
      if ((substr ($chromosome[$i], $j + $k, 1) eq 'A') ||      
          (substr ($chromosome[$i], $j + $k, 1) eq 'T'))
      {
        $AT++;
      }
    }

    my $AT_value_of_curent_window;
    $AT_value_of_curent_window = sprintf "%3.2f ", $AT / $current_window;
    $AT_content[$i] .= $AT_value_of_curent_window;
  }
}

# Now we print the obtained results for each chromosome.
#
foreach my $i (1..$NUMBER_OF_CHROMOSOMES)
{
  my $AT = 0;

  for (my $j = 0; $j < length $chromosome[$i]; $j++)
  {
    if ((substr ($chromosome[$i], $j, 1) eq 'A') ||      
        (substr ($chromosome[$i], $j, 1) eq 'T'))
    {
      $AT++;
    }
  }
 
  printf "Chromosome %2d size: %d\n", $i, length $chromosome[$i];
  printf "Chromosome %2d AT-content: %3.2f\n", $i, $AT / length $chromosome[$i];
  printf "%s\n", $AT_content[$i];
}

# End of program.
#
exit 0;

