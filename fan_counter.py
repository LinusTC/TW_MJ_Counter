from dictionary import *
from values import *

class FanCounter:
    def __init__(self, winner_seat, winner_tiles, curr_wind):
        self.winner_seat = winner_seat
        self.winner_tiles = winner_tiles
        self.curr_wind = curr_wind
        self.logs = []
    
    def count_wind_value(self):
        value = 0
        has_wind = False
        small_wind = 0
        big_wind = 0
        wind_logs = []
        counted_pos = False        
        
        #Counts wind
        for key in self.winner_tiles:
            if key not in wind_dict:
                continue
            else:
                has_wind = True

                if self.winner_tiles[key] >= 2:
                    small_wind += 1

                if self.winner_tiles[key] >= 3:
                    big_wind += 1
                    value += wind_value
                    wind_logs.append(f"{key} +{wind_value}")

        #Checks small/big wind
        if small_wind == 3:
            value = small_3_wind_value
            wind_logs.clear()
            wind_logs.append(f"小三風 +{value}")

        if big_wind == 3:
            value = big_3_wind_value
            wind_logs.clear()
            wind_logs.append(f"大三風 +{value}")

        if small_wind == 4:
            value = small_4_wind_value
            wind_logs.clear()
            wind_logs.append(f"小四喜 +{value}")

        if big_wind == 4:
            value = big_4_wind_value
            wind_logs.clear()
            wind_logs.append(f"大四喜 +{value}")

        #Counts curr wind
        if self.curr_wind in self.winner_tiles and self.winner_tiles[self.curr_wind] == 3:
            value += wind_value
            wind_logs.append(f"正{self.curr_wind}圈 +{wind_wind_value}")

        #Counts seat position
        if seat_dict[self.winner_seat] in self.winner_tiles and self.winner_tiles[seat_dict[self.winner_seat]] == 3:
            value += wind_seat_value
            counted_pos = True
            wind_logs.append(f"正{seat_dict[self.winner_seat]}位 +{wind_seat_value}")

        self.logs.extend(wind_logs)

        return wind_value if has_wind == False else 0, has_wind, counted_pos

    def count_zfb_value(self):
        value = 0
        has_zfb = False
        small_3 = 0
        big_3 = 0
        zfb_logs = []

        for key in self.winner_tiles:
            if key not in zfb_dict:
                continue
            else:
                has_zfb = True
                
                if self.winner_tiles[key] > 1:
                    small_3 += 1
                    if self.winner_tiles[key] > 2:
                        value += zfb_value
                        zfb_logs.append(f"{key} +{zfb_value}")
                        big_3 += 1

        if small_3 == 3:
            value = small_3_zfb_value
            zfb_logs.clear()
            zfb_logs.append(f"小三元 +{small_3_zfb_value}")

        if big_3 == 3:
            value = big_3_zfb_value
            zfb_logs.clear()
            zfb_logs.append(f"大三元 +{big_3_zfb_value}")

        self.logs.extend(zfb_logs)

        return wind_value if has_zfb == False else 0, has_zfb
    
    def getLogs(self):
        return self.logs
