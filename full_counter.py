from flower_counter import FlowerCounter
from fan_counter import FanCounter
from deck_validator import DeckValidator
from values import *
from types_of_hu import *
from dictionary import *

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
        self.total_number_of_valid_decks = len(self.deckValidator.possibleDecks)
        self.curr_validated_tiles = self.deckValidator.possibleDecks[0] if self.total_number_of_valid_decks > 0 else []
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
        for i in range(self.total_number_of_valid_decks):

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

            #Check flower
            value, log, hu, has_flower, counted_flower_pos = self.c_flower()
            temp_value += value
            _add_to_log(log)
            if hu:
                break

            #Check 字
            value, log, has_fan, counted_wind_pos = self.c_fan()
            temp_value += value
            _add_to_log(log)
            
            #No flower and no 字
            if not has_flower and not has_fan:
                temp_value += noFlower_noZFB_nowind_value_add_on
                _add_to_log(f'無字無花再加 +{noFlower_noZFB_nowind_value_add_on}')

            #正花正位
            if counted_flower_pos and counted_wind_pos:
                temp_value += flower_wind_seat_value_add_on
                _add_to_log(f'正花正位再加 +{flower_wind_seat_value_add_on}')

            #16bd
            value, log = self.c_16bd()
            temp_value += value
            _add_to_log(log)

            #13 waist
            value, log = self.c_13waist()
            temp_value += value
            _add_to_log(log)

            #Ligu
            value, log = self.c_ligu()
            temp_value += value
            _add_to_log(log)

            #general eyes
            value, log = self.c_general_eyes()
            temp_value += value
            _add_to_log(log)

            #gong
            value, log = self.c_gong()
            temp_value += value            
            _add_to_log(log)

            #2 or 3 numbers only
            value, log = self.c_two_or_three_numbers_only(has_fan)
            temp_value += value            
            _add_to_log(log)

            #Only fan tiles
            value, log = self.c_only_fan()
            temp_value += value            
            _add_to_log(log)

            #Only 1 9 tiles
            value, log = self.c_only_one_or_nine(has_fan)
            temp_value += value            
            _add_to_log(log)

            #Test same house
            value, log = self.c_same_house(has_fan)
            temp_value += value            
            _add_to_log(log)                 

            self.curr_validated_tiles = self.deckValidator.possibleDecks[i]

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
        flower_value, has_flower, counted_pos = self.flowerCounter.count_flower_value()
        has_flower_hu = self.curr_validated_tiles['hu_type'] == flower_hu

        if not has_flower:
            value = flower_value
            log = f'無花 +{value}'
            return value, log, has_flower_hu, has_flower, counted_pos

        if (has_flower_hu):
            value = seven_flower_value if len(self.curr_validated_tiles['flowers']) == 7 else eight_flower_value
            log = f'花胡 +{value}'
            return value, log, has_flower_hu, has_flower, counted_pos
        
        if has_flower:
            value = flower_value
            log = self.flowerCounter.getLogs()
            return value, log, has_flower_hu, has_flower, counted_pos

        return 0, None, False, False, False
    
    def c_fan(self):
        wind_total_value, has_wind, counted_pos = self.fanCounter.count_wind_value()
        zfb_value, has_zfb = self.fanCounter.count_zfb_value()
        has_fan = has_wind or has_zfb

        if not has_wind and not has_zfb:
            value = wind_total_value
            log = f'無字 +{value}'
            return value, log, has_fan, counted_pos
        
        value = wind_total_value + zfb_value
        log = self.fanCounter.getLogs()
        return value, log, has_fan, counted_pos
    
    def c_16bd(self):
        if self.curr_validated_tiles['hu_type'] == sixteen_bd_hu:
            value = sixteenbd_value
            log = f'16不搭 +{value}'
            return value, log
        
        return 0, None
    
    def c_13waist(self):
        if self.curr_validated_tiles['hu_type'] == thirteen_waist_hu:
            value = thirteen_waist_value
            log = f'13么/腰 +{value}'
            return value, log
        
        return 0, None
    
    def c_ligu(self):
        if self.curr_validated_tiles['hu_type'] == ligu_hu:
            value = li_gu_value
            log = f'Ligu +{value}'
            return value, log
        
        return 0, None
    
    def c_general_eyes(self):
        if self.curr_validated_tiles['eyes'] is not None and self.curr_validated_tiles['eyes'] not in zfb_dict and self.curr_validated_tiles['eyes'] not in wind_dict: 
            eyes_value = int(self.curr_validated_tiles['eyes'][1])
            if eyes_value == 2 or eyes_value == 5 or eyes_value == 8:
                value = general_eye_value
                log = f'將眼 +{value}'
                return value, log            
        return 0, None
    
    def c_gong(self):
        value = 0
        log = None
        for tile_group in self.curr_validated_tiles['tiles']:
            tile_group = tile_group if isinstance(tile_group, list) else [tile_group]
            if len(tile_group) == 4:
                value += gong_value

        log = f'槓 +{value}' if value > 0 else None

        return value, log
    
    def c_two_or_three_numbers_only(self, has_fan):
        number_set = set()
        
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            for tile in tiles:
                if tile in zfb_dict or tile in wind_dict:
                    continue
                number_set.add(tile[1])
        if len(number_set) == 3 and has_fan:
            value = three_numbers_fan_value
            log = f'三数 有番子 +{value}'
            return value, log
        
        if len(number_set) == 3 and not has_fan:
            value = three_numbers_no_fan_value
            log = f'三数 無番子 +{value}'
            return value, log
        
        if len(number_set) == 2 and has_fan:
            value = two_numbers_fan_value
            log = f'兩数 有番子 +{value}'
            return value, log
        
        if len(number_set) == 2 and not has_fan:
            value = two_numbers_no_fan_value
            log = f'兩数 無番子 +{value}'
            return value, log
        
        return 0, None
        
    def c_only_fan(self):
        for tile_group in self.curr_validated_tiles['tiles']:
            for tile in tile_group:
                if tile not in zfb_dict or tile not in wind_dict:
                    return 0, None

        value = only_fan_value
        log = f'全番子 +{value}'        
        return value, log

    def c_only_one_or_nine(self, has_fan):
        number_set = set()
        
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            for tile in tiles:
                if tile in zfb_dict or tile in wind_dict:
                    continue
                number_set.add(tile[1])
        
        for num in number_set:
            if num not in ('1', '9'):
                return 0, None
        
        value = one_nine_with_fan_value if has_fan else only_one_nine_value
        log = f'全么/腰九 有番子 +{value}' if has_fan else f'全么/腰九 無番子 +{value}'
        return value, log
    
    def c_same_house(self, has_fan):
        house_set = set()
        
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            for tile in tiles:
                if tile in zfb_dict or tile in wind_dict:
                    continue
                house_set.add(tile[0])
        
        if len(house_set) > 1:
            return 0, None
        
        value = same_house_with_fan_value if has_fan else all_same_house_value
        log = f'混一色 +{value}' if has_fan else f'清一色 +{value}'
        return value, log