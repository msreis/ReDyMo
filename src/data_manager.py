""" This file is part of ReDyMo.

    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.
    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.
    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.

"""

import sqlite3
from math import ceil

## @package ReDyMo.src.data_manager
# Contains the class DataManager.


## The DataManager class handles all input and loading of data.
# 
# It stores Chromosome data, activation probabilities of replication origins
# and information about Transcription Regions.
class DataManager:

  ## The constructor.
  # @param database_path The path to the sqlite3 database file containing
  # chromosome and transcription region data.
  # @param mfa_seq_folder_path Path for the MFA-Seq data on the replication
  # origin activation probability landscape.
  def __init__(self, database_path, mfa_seq_folder_path):
    self.database_path = database_path
    self.mfa_seq_folder_path = mfa_seq_folder_path

#-----------------------------------------------------------------------------#

  ## Fetches all chromosomes from database that match the filters in kwargs.
  # @param kwargs Array of organism-name pairs to filter the data. Only tuples
  # where property organism == name will be retrieved.
  def select_chromosomes_from_database(self, **kwargs):

    db = sqlite3.connect(self.database_path)
    cursor = db.cursor()
    for organism, name in kwargs.items():
      query = 'SELECT * FROM Chromosome WHERE ' + organism + ' = ?'
      cursor.execute(query, (name,))

    chromosome_tuples = cursor.fetchall()
    db.close()
    return chromosome_tuples

#-----------------------------------------------------------------------------#

  """ Generates the probability landscape for origin trigger from MFA-Seq data.
  """
  ## Generates the probability landscape for replication origin activation.
  # It reads the MFA-Seq files correspondent to the given code.
  # @param code Code to find the appropriate MFA-Seq score file.
  # @param length The length of the chromosome that this probability landscape
  # belongs to.
  def probability_landscape(self, code, length):

    scores = []
    with open(self.mfa_seq_folder_path + code + '.txt') as mfa_seq_file:
      for line in mfa_seq_file:
        scores.append(float(line))

    probability_landscape = [0] * length
    step = int(ceil(length/len(scores)))

    a = float((1 - 10**-4)/(max(scores) - min(scores)))
    b = 1 - (max(scores) * a)

    with open(self.mfa_seq_folder_path + code + '_probability.txt', 'w')\
    as probability_file:
      for i, score in enumerate(scores):
        probability = a * score + b
        probability_file.write("{}\n".format(probability))
        for j in range(i * step, (i + 1) * step):
          probability_landscape[j] = probability
          if j == length - 1:
            return probability_landscape

#-----------------------------------------------------------------------------#

  """ Final list of chromosome data that will be used by the simulation. """
  ## Assembles the final Chromosomes by appending all data about it.
  # @param organism The organism which to pick chromosome data from the
  # database and MFA-Seq.
  # @return An array of chromosomes stored as tuples.
  def chromosomes(self, organism):

    chromosomes = []
    chromosome_tuples =self.select_chromosomes_from_database(organism=organism)

    for t in chromosome_tuples:

      transcription_tuples = self.select_transcription_regions_from_database\
      (chromosome_code=t[0])

      constitutive_origins = self.select_constitutive_origins_from_database\
      (chromosome_code=t[0])

      chromosomes.append({'code': t[0],
                        'length': t[1],
         'probability_landscape': self.probability_landscape(code = t[0],\
                                                           length = t[1]),
         'transcription_regions': [{'start': d[0], 'end': d[1]}\
         for d in transcription_tuples],
         'constitutive_origins' : constitutive_origins})

    return chromosomes

#-----------------------------------------------------------------------------#

  ## Queries the database and gathers transcription regions according to the
  # arguments.
  # @param kwargs Array of  pairs to filter the queried data.
  # @return An array of transcription regions stored as tuples.
  def select_transcription_regions_from_database(self, **kwargs):  
    
    db = sqlite3.connect(self.database_path)
    cursor = db.cursor()
    
    for chromosome_code, code in kwargs.items():
      query = 'SELECT * FROM TranscriptionRegion WHERE ' + chromosome_code + ' = ?'
      cursor.execute(query, (code,))

    transcription_tuples = cursor.fetchall()
    db.close()

    return transcription_tuples

#-----------------------------------------------------------------------------#

  ## Queries the database and gathers constitutive origins according to the
  # arguments.
  # @param kwargs Array of chromosome_code-code pairs to filter the queried data.
  # @return An array of constitutive origins stored as tuples.
  def select_constitutive_origins_from_database(self, **kwargs):  
    
    db = sqlite3.connect(self.database_path)
    cursor = db.cursor()
    
    for chromosome_code, code in kwargs.items():
      query = 'SELECT position FROM ReplicationOrigin WHERE ' + chromosome_code + ' = ?'
      cursor.execute(query, (code,))

    constitutive_origins = cursor.fetchall()
    db.close()

    return constitutive_origins

#-----------------------------------------------------------------------------#

