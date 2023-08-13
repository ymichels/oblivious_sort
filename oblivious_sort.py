from RAM import RAM
from config import Config
from obliviousSort.oblivous_balls_into_bins import obliviousBallsIntoBins
from obliviousSort.extract_balls import extract_balls
from obliviousSort.merge_sort import merge_sort
def oblivious_sort():
    conf = Config()
    arr = RAM(1_000)
    for i in range(1_000):
        arr.memory[1_000-1-i] = i.to_bytes(conf.KEY_SIZE,'big') + b'\x01'*(conf.BLOCK_SIZE - conf.KEY_SIZE)
    arr = obliviousBallsIntoBins(conf, arr)
    arr = extract_balls(conf, arr, 1_000)
    merge_sort(conf, arr, 0, arr.getSize())
    for i in arr.memory[:180]:
        print(int.from_bytes(i[14:16], 'big', signed=False))


oblivious_sort()
print('done!')