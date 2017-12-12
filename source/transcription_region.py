from source.transcription_fork import TranscriptionFork


class TranscriptionRegion:
    def __init__(self, start, end, frequency):
        self.start = start - 1
        self.end = end - 1
        self.direction = int((end - start)/abs(end - start))
        self.period = 1/frequency
        self.timer = 0.0

    def spawn_fork(self, interval):
        if self.timer > self.period:
            self.timer = 0.0
            return(TranscriptionFork(speed=40,
                                     direction=self.direction,
                                     end=self.end,
                                     base=self.start))
        else:
            self.timer += interval
            return None
