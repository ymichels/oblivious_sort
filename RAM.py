import math

class RAM:
    dummey_note = b'\x00'
    def __init__(self, size) -> None:
        self.memory = [self.dummey_note] * size
    
    def getSize(self):
        return len(self.memory)


    def readBall(self, location):
        return self.memory[int(location)]


    def writeBall(self, location, ball):
        self.memory[int(location)] = ball
    
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
        
        

    def readChunks(self, chunks):
        balls = []
        for chunk in chunks:
            chunk_balls = self.readChunk(chunk)
            balls.extend(chunk_balls)
        return balls

    def writeChunks(self, chunks, balls):
        i = 0
        for chunk in chunks:
            start, end = chunk
            balls_num = math.ceil((end-start))
            self.writeChunk(chunk, balls[i:i+balls_num])
            i += balls_num
        return balls

    def readBalls(self, locations):
        return [self.readBall(location) for location in locations]
    
    def writeBalls(self, locations, balls):
        return [self.writeBall(location, ball) for location,ball in zip(locations,balls)]
