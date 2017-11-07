from source.replication_fork import ReplicationFork


class ForkManager:
    def __init__(self, size, genome, speed):
        self.replication_forks = list()
        for i in range(size):
            self.replication_forks.append(ReplicationFork(genome=genome, speed=speed))

        self.just_unattached = dict()
        for fork in self.replication_forks:
            self.just_unattached[fork] = False

        self.number_of_free_forks = size

    def advance_attached_forks(self):
        for fork in self.replication_forks:
            if self.just_unattached[fork]:
                self.just_unattached[fork] = False
                self.number_of_free_forks += 1

            if fork.is_attached():
                if not fork.advance():
                    self.just_unattached[fork] = True

    def attach_forks(self, genomic_location):
        number_of_forks_attached_to_this_location = 0
        direction = 1
        for fork in self.replication_forks:
            if not fork.is_attached() and not self.just_unattached[fork]:
                fork.attach(genomic_location=genomic_location, direction=direction)
                number_of_forks_attached_to_this_location += 1
                direction = - direction
                if number_of_forks_attached_to_this_location == 2:
                    break

        self.number_of_free_forks -= number_of_forks_attached_to_this_location
