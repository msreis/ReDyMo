class ReplicationFork:
    def __init__(self, genome, speed, boundaries):
        self.genome = genome
        self.speed = speed
        self.boundaries = boundaries
        self.base = None
        self.chromosome = None
        self.direction = None

    def attach(self, genomic_location, direction, time):
        if self.is_attached():
            raise ValueError("Tried to attach an already attached fork")

        self.base = genomic_location.base
        self.chromosome = genomic_location.chromosome
        self.direction = direction

        self.chromosome.replicate(start=self.base,
                                  end=self.base,
                                  time=time)

    def unattach(self):
        self.base = None
        self.chromosome = None
        self.direction = None

    def advance(self, time, interval):
        new_base = self.base + self.speed * self.direction * interval
        if new_base < 0:
            new_base = 0
            self.chromosome.unattach_replication(base=new_base)
        if not self.chromosome.replicate(start=self.base,
                                         end=new_base,
                                         time=time):
            self.unattach()
            return False

        self.base = new_base
        return True

    def is_attached(self):
        return self.base is not None

    def is_outside_boundaries(self, base):
        return not self.boundaries[0] <= base <= self.boundaries[1]
