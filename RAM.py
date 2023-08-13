import math

class RAM:
    dummey_note = b'\x00'
    def __init__(self, size) -> None:
        self.memory = [self.dummey_note] * size
    
    def getSize(self):
        return len(self.memory)
    
    def readChunk(self, chunk):
        start, end = chunk
        balls_num = int((end-start))
        return self.memory[int(start):int(end)]
    
    def writeChunk(self, chunk, balls):
        start, end = chunk
        balls_num = int((end-start))
        ball_start = int(start)
        if ball_start >= len(self.memory):
            self.memory.extend(balls)
        else:
            self.memory[ball_start:ball_start + len(balls)] = balls