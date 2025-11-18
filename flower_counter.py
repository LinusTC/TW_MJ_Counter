from dictionary import *

class FlowerCounter:
    def __init__(self, winner_seat, winner_cards):
        self.winner_seat = winner_seat
        self.winner_cards = winner_cards
    
    def count_flower(self):
        count = 0
        has_flower = False

        for key in self.winner_cards:
            if key not in flower_dict:
                continue
            else:
                has_flower = True
                count += 1

                if flower_dict[key] == self.winner_seat:
                    count += 1
        
        return count, has_flower