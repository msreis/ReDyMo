import math
import random
from source.replication_fork import ReplicationFork


class Chromosome:
    def __init__(self, code, length, probability_landscape, replication_speed, transcription_regions):
        self.code = code
        self.length = length
        self.replication_speed = replication_speed

        self.strand = [0] * self.length
        self.activation_probabilities = probability_landscape
        self.number_of_replicated_bases = 0
        self.number_of_origins = 0
        self.replication_forks = dict()
        self.transcription_forks = list()
        self.transcription_regions = transcription_regions

    def __len__(self):
        return self.length

    def __str__(self):
        chromosome_string = ""
        for i in range(0, len(self.strand), 500):
            chromosome_string += "{}\n".format(str(self.strand[i]))

        return chromosome_string

    def unattach_replication(self, base):
        for i, replication in enumerate(self.replication_forks):
            if replication.base == base:
                del self.replication_forks[i]

            break

    def attach_transcription(self, fork):
        if fork is None:
            return False

        self.transcription_forks.append(fork)
        fork.is_spawn_duplicated = self.is_base_replicated(base=fork.base)
        return True

    def attach_replication(self, base, time):
        if base + 1 >= self.length or self.strand[base] or self.strand[base + 1]\
                or random.random() >= self.activation_probabilities[base]:
            return False  # Nothing was attached

        self.number_of_origins += 1
        self.replication_forks[base] = ReplicationFork(base=base, direction=-1, speed=self.replication_speed)
        self.replication_forks[base + 1] = ReplicationFork(base=base, direction=+1, speed=self.replication_speed)
        self.replicate(start=base, end=base+1, time=time)
        return True

    def advance_transcriptions(self, interval):
        for transcription in self.transcription_forks:
            for i in range(transcription.base,
                           transcription.base + transcription.speed * transcription.direction * interval,
                           transcription.direction):
                if transcription.is_outside_boundaries(base=i):
                    self.transcription_forks.remove(transcription)
                    break

                if transcription.is_spawn_duplicated != self.is_base_replicated(base=i):
                    self.transcription_forks.remove(transcription)
                    self.replication_forks.pop(i, default=None)

    def unattach_transcription(self, base):
        removed_transcription = None
        for i, transcription in enumerate(self.transcription_forks):
            if transcription.base == base:
                removed_transcription = self.transcription_forks.pop(i)
                break

        for i, replication in enumerate(self.replication_forks):
            if replication.base == base:
                if replication.direction != removed_transcription.direction:
                    del self.replication_forks[i]

                break

    def is_base_replicated(self, base):
        return bool(self.strand[base])

    def replicate(self, start, end, time):
        direction = int(math.copysign(1, end - start))
        for i in range(start, end + direction, direction):
            if not self.strand[i]:
                self.strand[i] = time * direction
                self.number_of_replicated_bases += 1

    def is_replicated(self):
        return self.number_of_replicated_bases == len(self)
