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


class DataManager:

  def __init__(self, database_path, mfa_seq_folder_path):
    self.database_path = database_path
    self.mfa_seq_folder_path = mfa_seq_folder_path

#-----------------------------------------------------------------------------#

  def select_chromosomes_from_database(self, **kwargs):

    db = sqlite3.connect(self.database_path)
    cursor = db.cursor()
    for key, value in kwargs.items():
      query = 'SELECT * FROM Chromosome WHERE ' + key + ' = ?'
      cursor.execute(query, (value,))

    chromosome_tuples = cursor.fetchall()
    db.close()
    return chromosome_tuples

#-----------------------------------------------------------------------------#

  """ Generates the probability landscape for origin trigger from MFA-Seq data.
  """
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

  def chromosomes(self, organism):

    chromosomes = []
    chromosome_tuples =self.select_chromosomes_from_database(organism=organism)
    for t in chromosome_tuples:
      transcription_tuples = self.select_transcription_regions_from_database\
      (chromosome_code=t[0])

      chromosomes.append({'code': t[0],
                        'length': t[1],
         'probability_landscape': self.probability_landscape(code = t[0],\
                                                           length = t[1]),
         'transcription_regions': [{'start': d[0], 'end': d[1]}\
         for d in transcription_tuples]})

    return chromosomes

#-----------------------------------------------------------------------------#

  # Load polycistronic regions location data.
  #
  def select_transcription_regions_from_database(self, **kwargs):  
    
    db = sqlite3.connect(self.database_path)
    cursor = db.cursor()
    
    for key, value in kwargs.items():
      query = 'SELECT * FROM TranscriptionRegion WHERE ' + key + ' = ?'
      cursor.execute(query, (value,))

    transcription_tuples = cursor.fetchall()
    db.close()
    return transcription_tuples

#-----------------------------------------------------------------------------#

