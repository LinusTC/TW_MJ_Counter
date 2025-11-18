from dictionary import *

class FanCounter:
    def __init__(self, winner_seat, winner_cards, curr_circle):
        self.winner_seat = winner_seat
        self.winner_cards = winner_cards
        self.curr_circle = curr_circle
    
    def count_compass(self):
        count = 0
        has_compass = False
        
        #Counts compass
        for key in self.winner_cards:
            if key not in compass_dict:
                continue
            else:
                has_compass = True
                if self.winner_cards[key] >= 3:
                    count += 1

        #Counts curr circle
        if self.curr_circle in self.winner_cards and self.winner_cards[self.curr_circle] == 3:
            count += 1

        #Counts seat position
        if seat_dict[self.winner_seat] in self.winner_cards and self.winner_cards[seat_dict[self.winner_seat]] == 3:
            count += 1

        return count, has_compass

    def count_zfb(self):
        count = 0
        has_zfb = False
        small_3 = 0
        big_3 = 0

        for key in self.winner_cards:
            if key not in zfb_dict:
                continue
            else:
                has_zfb = True
                count += 2

                small_3 += 1
                if self.winner_cards[key] == 3:
                    big_3 += 1

        if small_3 == 3:
            count = 30

        if big_3 == 3:
            count = 60

        return count, has_zfb