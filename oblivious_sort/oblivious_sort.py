from RAM import RAM
from config import Config
from oblivious_sort.oblivous_balls_into_bins import oblivious_balls_into_bins
from oblivious_sort.extract_balls import extract_balls
from oblivious_sort.merge_sort import merge_sort
def oblivious_sort(ram: RAM, conf: Config) -> RAM:
    ram = oblivious_balls_into_bins(conf, ram)
    ram = extract_balls(conf, ram, 1_000)
    merge_sort(conf, ram, 0, ram.get_size())
    return ram