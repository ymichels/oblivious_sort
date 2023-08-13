from config import Config
import math
from RAM import RAM


def isBitOn(number, bit_num):
    return (number & (2**bit_num)) > 0

def key_to_pseudo_random_number(config: Config, key,limit=-1):
        if len(key) % Config.KEY_SIZE != 0:
            key += b'\x00'*(Config.KEY_SIZE - len(key) % Config.KEY_SIZE)
        enc = config.CIPHER.encrypt(key)
        if limit == -1:
            return int.from_bytes(enc, 'big', signed=False)
        return int.from_bytes(enc, 'big', signed=False) % limit

def split_to_bins_by_bit(config:Config, blocks, bit_num, number_of_bins):
    bin_zero = []
    bin_one = []
    for block in blocks:
        if block == RAM.dummey_note:
            continue
        assigned_bin = key_to_pseudo_random_number(config, block[:config.KEY_SIZE], number_of_bins)
        bit = isBitOn(assigned_bin, bit_num)
        if bit:
            bin_one.append(block)
        else:
            bin_zero.append(block)
    bin_one.extend([RAM.dummey_note] * (config.BIN_SIZE - len(bin_one)))
    bin_zero.extend([RAM.dummey_note] * (config.BIN_SIZE - len(bin_zero)))
    return bin_zero, bin_one


def oblivious_balls_into_bins(config:Config, array:RAM):
    current_ram = _oblivious_balls_into_bins_first_iteration(config, array)
    next_ram = RAM(current_ram.get_size())
    for bit_num in range(1,math.ceil(math.log(current_ram.get_size()/config.BIN_SIZE,2))):
        first_bin_index = 0
        for bin_index in range(math.ceil((current_ram.get_size()/config.BIN_SIZE)/2)):
            first_bin = current_ram.read_chunk((first_bin_index*config.BIN_SIZE, (first_bin_index + 1)*config.BIN_SIZE))
            second_bin = current_ram.read_chunk(
                ((first_bin_index + 2**bit_num)*config.BIN_SIZE, (first_bin_index + (2**bit_num) + 1)*config.BIN_SIZE))
            bin_zero, bin_one = split_to_bins_by_bit(config, first_bin + second_bin, math.ceil(math.log(current_ram.get_size()/config.BIN_SIZE,2)) - 1 - bit_num, math.ceil(current_ram.get_size()/config.BIN_SIZE))
            
            next_ram.write_chunk(
                (bin_index*2*config.BIN_SIZE, (bin_index +1)*2*config.BIN_SIZE), bin_zero + bin_one)
            first_bin_index +=1
            if first_bin_index % 2**bit_num == 0:
                first_bin_index += 2**bit_num
        next_ram, current_ram = current_ram, next_ram
    return current_ram
    
def _oblivious_balls_into_bins_first_iteration(config:Config, array:RAM)->RAM:
    second_array = RAM(2**math.ceil(math.log(math.ceil(array.get_size()*2/config.BIN_SIZE),2))*config.BIN_SIZE)

    current_read_pos = 0
    for bin_index in range(math.ceil(array.get_size()/config.BIN_SIZE)):
        balls = array.read_chunk((current_read_pos, current_read_pos + config.BIN_SIZE))
        bin_zero, bin_one = split_to_bins_by_bit(config, balls, math.ceil(math.log(math.ceil(second_array.get_size()/config.BIN_SIZE),2))-1, math.ceil(second_array.get_size()/config.BIN_SIZE))
        second_array.write_chunk(
            (2*current_read_pos, 2*current_read_pos + 2*config.BIN_SIZE), bin_zero + bin_one)
        current_read_pos += config.BIN_SIZE
    return second_array