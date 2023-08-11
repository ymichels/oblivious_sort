from RAM import RAM
from config import Config
from obliviousSort.oblivous_balls_into_bins import obliviousBallsIntoBins
def oblivious_sort():
    conf = Config()
    arr = RAM(1_000)
    for i in range(1_000):
        arr.memory[1_000-1-i] = i.to_bytes(conf.KEY_SIZE,'big') + b'\x01'*(conf.BLOCK_SIZE - conf.KEY_SIZE)
    arr = obliviousBallsIntoBins(conf, arr)
    for i in arr.memory[-180:]:
        print(int.from_bytes(i[14:16], 'big', signed=False)%64)


oblivious_sort()
print('done!')