import sqlite3
from math import ceil


class DataManager:
    def __init__(self, database_path, mfa_seq_folder_path):  # TODO: Include MFA-Seq data in database
        self.database_path = database_path
        self.mfa_seq_folder_path = mfa_seq_folder_path

    def select_chromosomes_from_database(self, **kwargs):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        for key, value in kwargs.items():
            query = 'SELECT * FROM Chromosome WHERE ' + key + ' = ?'
            cursor.execute(query, (value,))

        chromosome_tuples = cursor.fetchall()
        db.close()
        return chromosome_tuples

    def select_transcription_regions_from_database(self, **kwargs):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        for key, value in kwargs.items():
            query = 'SELECT * FROM TranscriptionRegion WHERE ' + key + ' = ?'
            cursor.execute(query, (value,))

        transcription_tuples = cursor.fetchall()
        db.close()
        return transcription_tuples

    def probability_landscape(self, code, length):
        scores = []
        with open(self.mfa_seq_folder_path + code + '.txt') as mfa_seq_file:
            for line in mfa_seq_file:
                scores.append(float(line))

        probability_landscape = [0] * length
        step = int(ceil(length/len(scores)))

        a = float((1 - 10**-4)/(max(scores) - min(scores)))
        b = 1 - (max(scores) * a)
        with open(self.mfa_seq_folder_path + code + '_probability.txt', 'w') as probability_file:
            for i, score in enumerate(scores):
                probability = a * score + b
                probability_file.write("{}\n".format(probability))
                for j in range(i * step, (i + 1) * step):
                    probability_landscape[j] = probability
                    if j == length - 1:
                        return probability_landscape

    def chromosomes(self, organism):
        chromosomes = []
        chromosome_tuples = self.select_chromosomes_from_database(organism=organism)
        for t in chromosome_tuples:
            transcription_tuples = self.select_transcription_regions_from_database(chromosome_code=t[0])

            chromosomes.append({'code': t[0],
                                'length': t[1],
                                'probability_landscape': self.probability_landscape(code=t[0], length=t[1]),
                                'transcription_regions': [{'start': d[0], 'end': d[1]} for d in transcription_tuples]})

        return chromosomes
