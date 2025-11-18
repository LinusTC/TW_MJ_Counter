from dictionary import *
from values import *

class FlowerCounter:
    def __init__(self, winner_seat, winner_cards):
        self.winner_seat = winner_seat
        self.winner_cards = winner_cards
        self.logs = []

    def count_flower(self):
        count = 0
        has_flower = False

        for key in self.winner_cards:
            if key not in flower_dict:
                continue
            else:
                has_flower = True
                count += flower_value
                self.logs.append(f"Flower {key} + {flower_value}")

                if flower_dict[key] == self.winner_seat:
                    count += flower_seat_value
                    self.logs.append(f"Flower {key} position + {flower_seat_value}")

        return count, has_flower
    
    def getLogs(self):
        return self.logs