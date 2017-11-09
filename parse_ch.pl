#!/usr/bin/perl -w

use strict;

my $line = <STDIN>;

chomp $line;

my @chromosome = split "\t", $line;

my $bin_sum = 0;
my $bin_count = 0;
my $bin_number = 0;

foreach my $nt (@chromosome)
{
  $bin_count++;

  if ($bin_count == 501)
  {
    $bin_number++;
    $bin_sum += $nt;
    printf $bin_number . " , %.2f\n", $bin_sum / 500;
    $bin_sum = $bin_count = 0;
  }
  else
  {
    $bin_sum += $nt;
  }
}

exit 0;
