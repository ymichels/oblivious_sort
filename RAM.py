import math

class RAM:
    dummey_note = b'\x00'
    def __init__(self, size) -> None:
        self.memory = [self.dummey_note] * size
    
    def get_size(self):
        return len(self.memory)
    
    def read_chunk(self, chunk):
        start, end = chunk
        return self.memory[int(start):int(end)]
    
    def write_chunk(self, chunk, balls):
        start, _ = chunk
        ball_start = int(start)
        if ball_start >= len(self.memory):
            self.memory.extend(balls)
        else:
            self.memory[ball_start:ball_start + len(balls)] = balls