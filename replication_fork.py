class ReplicationFork:
    def __init__(self, genome, speed):
        self.genome = genome
        self.speed = speed

        self.base = None
        self.chromosome = None
        self.direction = None

    def attach(self, genomic_location, direction):
        if self.is_attached():
            raise ValueError("Tried to attach an already attached fork")

        self.base = genomic_location.base
        self.chromosome = genomic_location.chromosome
        self.direction = direction

        self.chromosome.replicate(start=self.base,
                                  end=self.base)

    def unattach(self):
        self.base = None
        self.chromosome = None
        self.direction = None

    def advance(self):
        new_base = self.base + self.speed * self.direction

        if not self.chromosome.replicate(start=self.base,
                                         end=new_base):
            self.unattach()
            return False

        self.base = new_base
        return True

    def is_attached(self):
        return self.base is not None
