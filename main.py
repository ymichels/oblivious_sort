from RAM import RAM
from config import Config
from oblivious_sort.oblivious_sort import oblivious_sort

conf = Config()
ram = RAM(1_000)
# Create memory:
for i in range(1_000):
    # Each block is built as such: KEY | DATA (we put b'\x01' in the data)
    ram.memory[1_000-1-i] = i.to_bytes(conf.KEY_SIZE,'big') + b'\x01'*(conf.BLOCK_SIZE - conf.KEY_SIZE)

# Sort:
ram = oblivious_sort(ram, conf)

# Print the sorted keys
for block in ram.memory:
    print(int.from_bytes(block[:conf.KEY_SIZE], 'big', signed=False))

