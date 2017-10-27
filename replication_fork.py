class ReplicationFork:
    overall_replication_speed = 64  # bp/s

    def __init__(self, genome):
        self.genome = genome

        self.base = None
        self.chromosome = None
        self.speed = None

    def attach(self, genomic_location, direction):
        if self.is_attached():
            raise ValueError("Tried to attach an already attached fork")

        self.base = genomic_location.base
        self.chromosome = genomic_location.chromosome
        self.speed = ReplicationFork.overall_replication_speed * direction

        self.chromosome.replicate(start=self.base,
                                  end=self.base)

    def unattach(self):
        self.base = None
        self.chromosome = None
        self.speed = None

    def advance(self):
        new_base = self.base + self.speed

        if not self.chromosome.replicate(start=self.base,
                                         end=new_base):
            self.unattach()
            return False

        self.base = new_base
        return True

    def is_attached(self):
        return self.base is not None
