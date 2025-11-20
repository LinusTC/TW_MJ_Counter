from flower_counter import FlowerCounter
from fan_counter import FanCounter
from deck_validator import DeckValidator
from values import *
from types_of_hu import *

class FullCounter:
    def __init__(self, winner_tiles, winner_seat, current_wind, winning_tile, mo_myself):
        self.winner_tiles = winner_tiles
        self.winner_seat = winner_seat
        self.current_wind = current_wind
        self.winning_tile = winning_tile
        self.mo_myself = mo_myself
        self.deckValidator = DeckValidator(self.winner_tiles)
        self.flowerCounter = FlowerCounter(self.winner_seat, self.winner_tiles)
        self.fanCounter = FanCounter(self.winner_seat, self.winner_tiles, self.current_wind)
        self.valid = self.deckValidator.full_check()
        self.validated_tiles = self.deckValidator.possibleDecks
        self.final_value = 0
        self.logs = []

    def full_count(self):

        temp_value = 0
        temp_logs = []

        def _add_to_log(curr_log):
            if curr_log:
                if isinstance(curr_log, list):
                    temp_logs.extend(curr_log)
                else:
                    temp_logs.append(curr_log)
        
        for i in range(len(self.validated_tiles)):

            #Check bomb
            value, log, bomb_result = self.c_bomb_hu()
            if bomb_result:
                self.final_value = value
                _add_to_log(log)
                return self.final_value, self.logs
            
            #Check zi mo
            value, log = self.c_mo_myself()
            temp_value += value
            _add_to_log(log)

            #Check flower hu
            value, log, hu = self.c_flower()
            temp_value += value
            _add_to_log(log)
            if hu:
                break

        self.final_value = temp_value
        self.logs = temp_logs

        return self.final_value, self.logs
    
    def c_bomb_hu(self):
        if not self.valid:
            return -explode_hu_value, f'炸胡， 每家賠-{explode_hu_value}', True
        return 0, None, False
    
    def c_mo_myself(self):
        if self.mo_myself: 
            return myself_mo_value, f'自摸 +{myself_mo_value}'
        return 0, None

    def c_flower(self):
        flower_count, has_flower = self.flowerCounter.count_flower()

        if not has_flower:
            value = flower_value
            log = f'無花 +{value}'
            return value, log, False

        if (self.validated_tiles[0]['hu_type'] == flower_hu):
            value = seven_flower_value if len(self.validated_tiles[0]['flowers']) == 7 else eight_flower_value
            log = f'花胡 +{value}'
            return value, log, True
        
        if has_flower:
            value = flower_count
            log = self.flowerCounter.getLogs()
            return value, log, False

        return 0, None, False