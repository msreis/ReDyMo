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
        for i in range(0, len(self.strand), 1):
            a = "-" if not self.strand[i] else "*"
            chromosome_string += "{} ".format(a)

        return chromosome_string + "\n"

    def attach_transcription(self, fork):
        if fork is None:
            return False

        self.transcription_forks.append(fork)
        fork.is_spawn_duplicated = self.is_base_replicated(base=fork.base)
        return True

    def attach_replication(self, base, time):
        if base + 1 >= self.length or self.strand[base] or self.strand[base + 1]\
                or random.random() >= self.activation_probabilities[base]:
            return 0  # Nothing was attached

        self.number_of_origins += 1
        self.replication_forks[base] = ReplicationFork(base=base, direction=-1, speed=self.replication_speed)
        self.replication_forks[base + 1] = ReplicationFork(base=base, direction=+1, speed=self.replication_speed)
        self.replicate(start=base, end=base+1, time=time)
        return -2

    def advance_transcriptions(self, interval):
        freed_forks = 0
        for index, transcription in enumerate(self.transcription_forks):
            final_base = None
            for i in range(transcription.base,
                           transcription.base + transcription.speed * transcription.direction * interval,
                           transcription.direction):
                if transcription.is_outside_boundaries(base=i):
                    self.transcription_forks.pop(index)
                    break

                if transcription.is_spawn_duplicated != self.is_base_replicated(base=i):
                    self.transcription_forks.pop(index)

                    replication = self.replication_forks.pop(i, None)
                    if replication is not None:
                        freed_forks += 1

                    break

                final_base = i

            transcription.base = final_base
        return freed_forks

    def advance_replications(self, interval, time):
        freed_forks = 0
        for base, fork in self.replication_forks.items():
            final_base = None
            conflict = False

            for i in range(base,
                           base + fork.speed * fork.direction * interval,
                           fork.direction):
                if i < 0:
                    final_base = 0
                    conflict = True
                    break

                if i > len(self) - 1:
                    final_base = len(self) - 1
                    conflict = True
                    break

                if self.is_base_replicated(i):
                    final_base = i
                    conflict = True
                    break

                final_base = i

            self.replicate(start=base, end=final_base, time=time)
            if conflict:
                final_base = None
                freed_forks += 1

            fork.base = final_base

        new_dict = dict()
        for base, fork in self.replication_forks.items():
            if fork.base is not None:
                new_dict[fork.base] = fork

        self.replication_forks = new_dict

        return freed_forks

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
