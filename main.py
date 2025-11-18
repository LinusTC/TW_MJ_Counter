from dictionary import *
from fan_counter import FanCounter
from flower_counter import FlowerCounter

if __name__ == "__main__":
    test = {'ff1': 1, "f1": 1, 'f2': 1, 'west' : 3, 'east': 3, 'zhong': 3, 'fa': 3, 'bai': 2, 'north': 3}
    winner_seat = 2
    curr_circle = 'west'

    count = 0
    logs = []
    
    fan_counter = FanCounter(winner_seat, test, curr_circle)
    compas_count, has_compass = fan_counter.count_compass()
    zfb_count, has_zef = fan_counter.count_zfb()
    logs.append(fan_counter.getLogs())
    
    flower_counter = FlowerCounter(winner_seat, test)
    flower_count, has_flower = flower_counter.count_flower()
    logs.append(flower_counter.getLogs())

    count += compas_count + flower_count + zfb_count
    print(f"Total count: {count}")
    print("Logs:")
    for log_group in logs:
        for log in log_group:
            print(f"{log}")