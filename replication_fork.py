class ReplicationFork:
    overall_replication_speed = 64  # bp/s

    def __init__(self, genome):
        self.genome = genome

        self.attached_genomic_location = None
        self.speed = None

    def attach(self, genomic_location, direction):
        if self.is_attached:
            raise ValueError("Tried to attach an already attached fork")

        self.attached_genomic_location = genomic_location
        self.speed = ReplicationFork.overall_replication_speed * direction
        self.genome.duplicate(start=genomic_location, end=genomic_location)

    def unattach(self):
        self.attached_genomic_location = None
        self.speed = None

    def advance(self):
        chromosome = self.attached_genomic_location.chromosome
        if not chromosome.replicate(start=self.attached_genomic_location.base,
                                    end=self.attached_genomic_location.base + self.speed):
            self.unattach()
            return False

        return True

    def is_attached(self):
        return self.attached_genomic_location is not None
