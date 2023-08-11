from config import Config
import math
from RAM import RAM


def isBitOn(number, bit_num):
    return (number & (2**bit_num)) > 0

def keyToPseudoRandomNumber(config:Config, key,limit=-1):
        if len(key) % Config.KEY_SIZE != 0:
            key += b'\x00'*(Config.KEY_SIZE - len(key) % Config.KEY_SIZE)
        enc = key #config.CIPHER.encrypt(key)
        if limit == -1:
            return int.from_bytes(enc, 'big', signed=False)
        return int.from_bytes(enc, 'big', signed=False) % limit

def splitToBinsByBit(config:Config, blocks, bit_num, number_of_bins):
    bin_zero = []
    bin_one = []
    for block in blocks:
        if block == RAM.dummey_note:
            continue
        assigned_bin = keyToPseudoRandomNumber(config, block[:config.KEY_SIZE], number_of_bins)
        bit = isBitOn(assigned_bin, bit_num)
        if bit:
            bin_one.append(block)
        else:
            bin_zero.append(block)
    if config.BIN_SIZE - len(bin_zero) < 0:
        print('happened')
        config.count += len(bin_zero) - config.BIN_SIZE
    if config.BIN_SIZE - len(bin_one) < 0:
        print('happened')
        config.count += len(bin_one) - config.BIN_SIZE
    bin_one.extend([RAM.dummey_note] * (config.BIN_SIZE - len(bin_one)))
    bin_zero.extend([RAM.dummey_note] * (config.BIN_SIZE - len(bin_zero)))
    return bin_zero, bin_one


def obliviousBallsIntoBins(config:Config, array:RAM):
    current_ram = _obliviousBallsIntoBinsFirstIteration(config, array)
    next_ram = RAM(current_ram.getSize())
    for bit_num in range(1,math.ceil(math.log(current_ram.getSize()/config.BIN_SIZE,2))):
        first_bin_index = 0
        for bin_index in range(math.ceil((current_ram.getSize()/config.BIN_SIZE)/2)):
            first_bin = current_ram.readChunks([(first_bin_index*config.BIN_SIZE, (first_bin_index + 1)*config.BIN_SIZE)])
            second_bin = current_ram.readChunks([
                ((first_bin_index + 2**bit_num)*config.BIN_SIZE, (first_bin_index + (2**bit_num) + 1)*config.BIN_SIZE)])
            bin_zero, bin_one = splitToBinsByBit(config, first_bin + second_bin, math.ceil(math.log(current_ram.getSize()/config.BIN_SIZE,2)) - 1 - bit_num, math.ceil(current_ram.getSize()/config.BIN_SIZE))
            
            next_ram.writeChunks(
                [(bin_index*2*config.BIN_SIZE, (bin_index +1)*2*config.BIN_SIZE)], bin_zero + bin_one)
            first_bin_index +=1
            if first_bin_index % 2**bit_num == 0:
                first_bin_index += 2**bit_num
        next_ram, current_ram = current_ram, next_ram
    return current_ram
    
def _obliviousBallsIntoBinsFirstIteration(config:Config, array:RAM)->RAM:
    # second_array = RAM(2**array.getSize()*2)
    second_array = RAM(2**math.ceil(math.log(math.ceil(array.getSize()*2/config.BIN_SIZE),2))*config.BIN_SIZE)

    current_read_pos = 0
    for bin_index in range(math.ceil(array.getSize()/config.BIN_SIZE)):
        balls = array.readChunks([(current_read_pos, current_read_pos + config.BIN_SIZE)])
        bin_zero, bin_one = splitToBinsByBit(config, balls, math.ceil(math.log(math.ceil(second_array.getSize()/config.BIN_SIZE),2))-1, math.ceil(second_array.getSize()/config.BIN_SIZE))
        second_array.writeChunks(
            [(2*current_read_pos, 2*current_read_pos + 2*config.BIN_SIZE)], bin_zero + bin_one)
        current_read_pos += config.BIN_SIZE
    return second_array