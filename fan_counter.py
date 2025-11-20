from dictionary import *
from values import *

class FanCounter:
    def __init__(self, winner_seat, winner_tiles, curr_circle):
        self.winner_seat = winner_seat
        self.winner_tiles = winner_tiles
        self.curr_circle = curr_circle
        self.logs = []
    
    def count_wind(self):
        count = 0
        has_wind = False
        small_4 = 0
        big_4 = 0
        wind_logs = []        
        
        #Counts wind
        for key in self.winner_tiles:
            if key not in wind_dict:
                continue
            else:
                has_wind = True

                if self.winner_tiles[key] >= 2:
                    small_4 += 1

                if self.winner_tiles[key] >= 3:
                    big_4 += 1
                    count += wind_value
                    wind_logs.append(f"{key} +{wind_value}")

        #Checks small/big four wind
        if small_4 == 4:
            count = small_4_wind_value
            wind_logs.clear()
            wind_logs.append(f"Has small 4 wind +{small_4_wind_value}")

        if big_4 == 4:
            count = big_4_wind_value
            wind_logs.clear()
            wind_logs.append(f"Has big 4 wind +{big_4_wind_value}")

        #Counts curr circle
        if self.curr_circle in self.winner_tiles and self.winner_tiles[self.curr_circle] == 3:
            count += wind_circle_value
            wind_logs.append(f"Current circle is {self.curr_circle} +{wind_circle_value}")

        #Counts seat position
        if seat_dict[self.winner_seat] in self.winner_tiles and self.winner_tiles[seat_dict[self.winner_seat]] == 3:
            count += wind_seat_value
            wind_logs.append(f"wind seat position +{wind_seat_value}")

        self.logs.append(wind_logs)

        return count, has_wind

    def count_zfb(self):
        count = 0
        has_zfb = False
        small_3 = 0
        big_3 = 0
        zfb_logs = []

        for key in self.winner_tiles:
            if key not in zfb_dict:
                continue
            else:
                has_zfb = True
                count += zfb_value
                zfb_logs.append(f"Has {key} +{zfb_value}")

                small_3 += 1
                if self.winner_tiles[key] == 3:
                    big_3 += 1

        if small_3 == 3:
            count = small_3_zfb_value
            zfb_logs.clear()
            zfb_logs.append(f"Has small zfb +{small_3_zfb_value}")

        if big_3 == 3:
            count = big_3_zfb_value
            zfb_logs.clear()
            zfb_logs.append(f"Has big zfb +{big_3_zfb_value}")

        self.logs.append(zfb_logs)

        return count, has_zfb
    
    def getLogs(self):
        return self.logs
