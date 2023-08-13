from RAM import RAM
import random
from config import Config
def extract_balls(conf: Config, arr: RAM, orginial_size):
    read_position = 0
    write_position = 0
    result = RAM(orginial_size)
    while read_position < arr.getSize():
        bin = arr.readChunk((read_position, read_position + conf.BIN_SIZE))
        bin = [block for block in bin if block != RAM.dummey_note]
        random.shuffle(bin)
        result.writeChunk((write_position, write_position + len(bin)), bin)
        read_position += conf.BIN_SIZE
        write_position += len(bin)
    return result

