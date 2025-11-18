from dictionary import *
from values import *

class FanCounter:
    def __init__(self, winner_seat, winner_cards, curr_circle):
        self.winner_seat = winner_seat
        self.winner_cards = winner_cards
        self.curr_circle = curr_circle
        self.logs = []
    
    def count_compass(self):
        count = 0
        has_compass = False
        small_4 = 0
        big_4 = 0
        compass_logs = []        
        
        #Counts compass
        for key in self.winner_cards:
            if key not in compass_dict:
                continue
            else:
                has_compass = True

                if self.winner_cards[key] >= 2:
                    small_4 += 1

                if self.winner_cards[key] >= 3:
                    big_4 += 1
                    count += compass_value
                    compass_logs.append(f"{key} +{compass_value}")

        #Checks small/big four compass
        if small_4 == 4:
            count = small_4_compass_value
            compass_logs.clear()
            compass_logs.append(f"Has small 4 compass +{small_4_compass_value}")

        if big_4 == 4:
            count = big_4_compass_value
            compass_logs.clear()
            compass_logs.append(f"Has big 4 compass +{big_4_compass_value}")

        #Counts curr circle
        if self.curr_circle in self.winner_cards and self.winner_cards[self.curr_circle] == 3:
            count += compass_circle_value
            compass_logs.append(f"Current circle is {self.curr_circle} +{compass_circle_value}")

        #Counts seat position
        if seat_dict[self.winner_seat] in self.winner_cards and self.winner_cards[seat_dict[self.winner_seat]] == 3:
            count += compass_seat_value
            compass_logs.append(f"Compass seat position +{compass_seat_value}")

        self.logs.append(compass_logs)

        return count, has_compass

    def count_zfb(self):
        count = 0
        has_zfb = False
        small_3 = 0
        big_3 = 0
        zfb_logs = []

        for key in self.winner_cards:
            if key not in zfb_dict:
                continue
            else:
                has_zfb = True
                count += zfb_value
                zfb_logs.append(f"Has {key} +{zfb_value}")

                small_3 += 1
                if self.winner_cards[key] == 3:
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
