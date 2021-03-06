#!/bin/bash

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

# Using replisome speed measured for T. brucei TREU927 (61.66 bp/sec).
#
./calculate_maximum_transcription_frequency.pl 61.66 1064672 1 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 1193948 2 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 1653225 3 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 1590432 4 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 1802303 5 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 1618915 6 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 2205233 7 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 2481190 8 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 3542885 9 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 4144375 10 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 61.66 5223313 11 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta


# Using replisome speed measured for T. brucei Lister427 (30.66 bp/sec).
# However, the chromosome lengths used here are the ones from TREU927, since
# the MFA-seq data employed in this study were produced for the latter species.
# Nonetheless, chromosome lengths of both species are similar to each other.
#
./calculate_maximum_transcription_frequency.pl 30.66 1064672 1 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 1193948 2 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 1653225 3 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 1590432 4 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta
 
./calculate_maximum_transcription_frequency.pl 30.66 1802303 5 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 1618915 6 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 2205233 7 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 2481190 8 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 3542885 9 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 4144375 10 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

./calculate_maximum_transcription_frequency.pl 30.66 5223313 11 ../data/TriTrypDB-34_TbruceiTREU927_AnnotatedCDSs.fasta

