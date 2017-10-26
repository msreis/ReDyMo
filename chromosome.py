class Chromosome:
    def __init__(self, code, length):
        self.code = code
        self.length = length
        self.strand = [False] * self.length
        self.activation_probabilities = [.5] * self.length
        self.number_of_replicated_bases = 0

    def __len__(self):
        return self.length

    def activation_probability(self, base):
        return self.activation_probabilities[base]

    def replicate(self, start, end):
        is_normal_transcription = True
        if end < 0:
            is_normal_transcription = False
            end = 0

        elif end > len(self) - 1:
            is_normal_transcription = False
            end = len(self) - 1

        if end < start:
            start, end = end, start

        for i in range(start, end + 1):
            if self.strand[i]:
                is_normal_transcription = False
                break

            self.strand[i] = True
            self.number_of_replicated_bases += 1

        return is_normal_transcription

    def is_replicated(self):
        return self.number_of_replicated_bases == len(self)
