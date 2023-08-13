from RAM import RAM
import random
from config import Config

def copy_merged_to_arr(conf: Config, arr: RAM, merged: RAM, start, end):
    location = 0
    while location <= end - start:
        mem = merged.read_chunk((location, min(location + conf.LOCAL_MEMORY_SIZE, merged.get_size())))
        arr.write_chunk((start + location, start + min(location + conf.LOCAL_MEMORY_SIZE, merged.get_size())), mem)
        location += conf.LOCAL_MEMORY_SIZE


def merge(conf: Config, arr: RAM, start, end):
    written = 0
    middle = int((start + end)/2)
    left_pointer = start
    right_pointer = middle
    res = RAM(end - start)
    while written != end - start:
        left_array = arr.read_chunk((left_pointer, min(left_pointer + conf.BIN_SIZE, middle)))
        right_array = arr.read_chunk((right_pointer, min(right_pointer + conf.BIN_SIZE,end)))
        if min(len(left_array), len(right_array)) == 0:
            to_write = left_array if len(right_array) == 0 else right_array
            res.write_chunk((written, written + len(to_write)), to_write)
            break
        to_write = []
        i = j = 0
        while i < len(left_array) and j < len(right_array):
            if int.from_bytes(left_array[i][:conf.KEY_SIZE], 'big', signed=False) <= int.from_bytes(right_array[j][:conf.KEY_SIZE], 'big', signed=False):
                to_write.append(left_array[i])
                i += 1
            else:
                to_write.append(right_array[j])
                j += 1
        res.write_chunk((written, written + len(to_write)), to_write)
        left_pointer += i
        right_pointer += j
        written += len(to_write)
    copy_merged_to_arr(conf, arr, res, start, end)
        


def merge_sort(conf: Config, arr: RAM, start, end):
    if end-start <= conf.LOCAL_MEMORY_SIZE:
        array = arr.read_chunk((start, end))
        array.sort(key=lambda block: int.from_bytes(block[:conf.KEY_SIZE], 'big', signed=False))
        arr.write_chunk((start, end), array)
        return
    merge_sort(conf, arr, start, int((start + end)/2))
    merge_sort(conf, arr, int((start + end)/2), end)
    merge(conf, arr, start, end)

