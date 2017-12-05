class TranscriptionFork:
    def __init__(self, speed, direction, boundaries, chromosome):
        self.boundaries = boundaries
        self.base = boundaries[0]
        self.speed = speed
        self.direction = direction
        self.chromosome = chromosome

    def advance(self, interval):
        for i in range(self.base, self.base + self.speed * self.direction * interval + self.direction, self.direction):
            self.base = i
            if self.is_outside_boundaries(i):
                self.chromosome.unattach_transcription(i)
                break

            if self.chromosome.is_base_replicated(i):
                self.chromosome.unattach_transcription(i)
                break

    def is_outside_boundaries(self, base):
        return not self.boundaries[0] <= base <= self.boundaries[1]
