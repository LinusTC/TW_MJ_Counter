from dictionary import *
from fan_counter import FanCounter
from flower_counter import FlowerCounter

if __name__ == "__main__":
    test = {'west' : 3, 'east': 3, 'ff1': 1, "f1": 1, 'f2': 1, 'zhong': 3, 'fa': 3, 'bai': 3, 'north': 2}
    winner_seat = 2
    curr_circle = 'west'

    count = 0
    
    fan_counter = FanCounter(winner_seat, test, curr_circle)
    compas_count, has_compass = fan_counter.count_compass()
    zfb_count, has_zef = fan_counter.count_zfb()
    
    flower_counter = FlowerCounter(winner_seat, test)
    flower_count, has_flower = flower_counter.count_flower()

    count += compas_count + flower_count + zfb_count
    print(count)