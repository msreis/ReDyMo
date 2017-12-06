class TranscriptionFork:
    def __init__(self, speed, direction, end, base, chromosome):
        self.end = end
        self.speed = speed
        self.direction = direction

        self.base = base
        self.chromosome = chromosome
        self.is_spawn_duplicated = None

    def is_outside_boundaries(self, base):
        return not base * self.direction <= self.end * self.direction
