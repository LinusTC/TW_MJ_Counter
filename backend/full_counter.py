from flower_counter import FlowerCounter
from fan_counter import FanCounter
from deck_validator import DeckValidator
from helpers import *
from values import *
from types_of_hu import *
from dictionary import *

class FullCounter:
    def __init__(self, winner_tiles, winner_seat, current_wind, winning_tile, mo_myself, door_clear, base_value, multiplier):
        self.winner_tiles = winner_tiles
        self.winner_seat = winner_seat
        self.current_wind = current_wind
        self.winning_tile = winning_tile
        self.mo_myself = mo_myself
        self.door_clear = door_clear
        self.base_value = base_value
        self.multiplier = multiplier
        self.deckValidator = DeckValidator(self.winner_tiles)
        self.flowerCounter = FlowerCounter(self.winner_seat, self.winner_tiles)
        self.fanCounter = FanCounter(self.winner_seat, self.winner_tiles, self.current_wind)
        self.valid = self.deckValidator.full_check()
        self.total_number_of_valid_decks = len(self.deckValidator.possibleDecks)
        self.curr_validated_tiles = self.deckValidator.possibleDecks[0] if self.total_number_of_valid_decks > 0 else []
        self.final_value = 0
        self.logs = []

    def full_count(self):
        max_value = 0
        max_logs = []
        winning_deck = None
        winning_deck_organized = None

        def _add_to_log(curr_log, temp_logs):
            if curr_log:
                if isinstance(curr_log, list):
                    temp_logs.extend(curr_log)
                else:
                    temp_logs.append(curr_log)

        for i in range(self.total_number_of_valid_decks):
            temp_value = 0
            temp_logs = []
            self.curr_validated_tiles = self.deckValidator.possibleDecks[i]

            '-------------------------------------------------------------------------'
            '--------------------------------ALL COUNTS-------------------------------'
            '-------------------------------------------------------------------------'

            #Check bomb
            value, log, bomb_result = self.c_bomb_hu()
            if bomb_result:
                self.final_value = value
                _add_to_log(log, temp_logs)
                return self.final_value, temp_logs
            
            #Check zi mo and door clear
            value, log = self.c_door_clear_zimo()
            temp_value += value
            _add_to_log(log, temp_logs)
            #Check flower
            value, log, hu, has_flower, counted_flower_pos = self.c_flower()
            temp_value += value
            _add_to_log(log, temp_logs)
            if hu:
                if temp_value > max_value:
                    max_value = temp_value
                    max_logs = temp_logs
                    winning_deck = self.winner_tiles
                    winning_deck_organized = self.curr_validated_tiles
                continue

            #Check 字
            value, log, has_fan, counted_wind_pos = self.c_fan()
            temp_value += value
            _add_to_log(log, temp_logs)
            
            #No flower and no 字
            if not has_flower and not has_fan:
                temp_value += noFlower_noZFB_nowind_value_add_on
                _add_to_log(f'無字無花再加 +{noFlower_noZFB_nowind_value_add_on}', temp_logs)

            #正花正位
            if counted_flower_pos and counted_wind_pos:
                temp_value += flower_wind_seat_value_add_on
                _add_to_log(f'正花正位再加 +{flower_wind_seat_value_add_on}', temp_logs)

            #16bd
            value, log = self.c_16bd()
            temp_value += value
            _add_to_log(log, temp_logs)

            #13 waist
            value, log = self.c_13waist()
            temp_value += value
            _add_to_log(log, temp_logs)

            #Ligu
            value, log = self.c_ligu()
            temp_value += value
            _add_to_log(log, temp_logs)

            #duk duk, jia duk
            value, log = self.c_duk_duk_jia_duk_dui_pong()
            temp_value += value
            _add_to_log(log, temp_logs)

            #general eyes
            value, log = self.c_general_eyes()
            temp_value += value
            _add_to_log(log, temp_logs)

            #gong
            value, log = self.c_gong_or_4_turtle()
            temp_value += value            
            _add_to_log(log, temp_logs)

            #2 or 3 numbers only
            value, log = self.c_two_or_three_numbers_only(has_fan)
            temp_value += value            
            _add_to_log(log, temp_logs)

            #Only fan tiles
            value, log = self.c_only_fan()
            temp_value += value            
            _add_to_log(log, temp_logs)

            #Only 1 9 tiles
            value, log = self.c_only_one_or_nine(has_fan)
            temp_value += value            
            _add_to_log(log, temp_logs)

            #Break waist
            value, log = self.c_break_waist(has_fan)
            temp_value += value            
            _add_to_log(log, temp_logs)
            
            #Test same house
            value, log = self.c_same_house(has_fan)
            temp_value += value            
            _add_to_log(log, temp_logs)

            #2 house
            value, log = self.c_less_door(has_fan)
            temp_value += value            
            _add_to_log(log, temp_logs)

            #5 house
            value, log = self.c_5_doors()
            temp_value += value            
            _add_to_log(log, temp_logs)    

            #Test lao shao
            value, log = self.c_lao_shao()
            temp_value += value            
            _add_to_log(log, temp_logs)    

            #Test ban gao
            value, log = self.c_ban_gao()
            temp_value += value            
            _add_to_log(log, temp_logs)
            
            #Test sister
            value, log = self.c_sister()
            temp_value += value            
            _add_to_log(log, temp_logs)

            #Test sister pong
            value, log = self.c_sister_pong()
            temp_value += value            
            _add_to_log(log, temp_logs)

            #ping hu or dui dui hu
            value, log, type_of_hu = self.c_dui_dui_or_ping_hu()
            temp_value += value
            _add_to_log(log, temp_logs)

            if type_of_hu == 'ping_hu' and not has_flower and not has_fan:
                temp_value += no_zifa_ping_hu_value_add_on
                _add_to_log(f'無字花平胡再加 +{no_zifa_ping_hu_value_add_on}', temp_logs)

            #dragons
            value, log = self.c_dragons()
            temp_value += value
            _add_to_log(log, temp_logs)

            '-------------------------------------------------------------------------'

            # Add base and multiplier
            temp_value += self.base_value
            temp_value *= self.multiplier
            # Compare with max after processing this deck

            print(self.curr_validated_tiles, temp_value)

            if temp_value > max_value:
                max_value = temp_value
                max_logs = temp_logs
                winning_deck = self.winner_tiles
                winning_deck_organized = self.curr_validated_tiles

        self.final_value = max_value
        self.logs = max_logs

        return self.final_value, self.logs, winning_deck, winning_deck_organized
    
    def c_bomb_hu(self):
        if not self.valid:
            return -explode_hu_value, f'炸胡， 每家賠-{explode_hu_value}', True
        return 0, None, False
    
    def c_door_clear_zimo(self):
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        if self.mo_myself and self.door_clear and not is_special_hu: 
            return door_clear_zimo_value, f'門清自摸 +{door_clear_zimo_value}'
        if self.mo_myself: 
            return myself_mo_value, f'自摸 +{myself_mo_value}'
        if self.door_clear and not is_special_hu: 
            return door_clear_value, f'門清 +{door_clear_value}'
        return 0, None
    
    def c_duk_duk_jia_duk_dui_pong(self):
        if not self.winning_tile:
            return 0, None
            
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        if is_special_hu:
            return 0, None
        
        # Find all groups containing the winning tile
        groups_with_winning_tile = {}
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if self.winning_tile in tiles:
                remaining_tiles = tiles.copy()
                remaining_tiles.remove(self.winning_tile)
                groups_with_winning_tile[tuple(tiles)] = remaining_tiles

        possible_tiles_list = [
            find_tiles_that_complete_set(incomplete_group)
            for incomplete_group in groups_with_winning_tile.values()
        ]

        if len(groups_with_winning_tile) == 1:
            possible_tiles = possible_tiles_list[0]
            if len(possible_tiles['tiles']) == 1 and (possible_tiles['complete_type'] == shang or possible_tiles['complete_type'] == eyes):
                value = real_solo_value
                log = f'獨獨 +{real_solo_value}'
                return value, log

        if len(groups_with_winning_tile) > 1:
            for item in possible_tiles_list:
                if (item['complete_type'] == shang or item['complete_type'] == eyes) and len(item['tiles']) == 1:
                    value = fake_solo_value
                    log = f'假獨 +{fake_solo_value}'
                    return value, log

        for item in possible_tiles_list:
            if item['complete_type'] == pong:
                value = double_pong_value
                log = f'對碰 +{double_pong_value}'
                return value, log
            
        return 0, None
    
    def c_flower(self):
        flower_value, has_flower, counted_pos = self.flowerCounter.count_flower_value()
        has_flower_hu = self.curr_validated_tiles['hu_type'] == flower_hu

        if not has_flower:
            value = flower_value
            log = f'無花 +{value}'
            return value, log, has_flower_hu, has_flower, counted_pos

        if has_flower_hu:
            value = seven_flower_value if len(self.curr_validated_tiles['flowers']) == 7 else eight_flower_value
            log = f'花胡 +{value}'
            return value, log, has_flower_hu, has_flower, counted_pos
        
        if has_flower:
            value = flower_value
            log = self.flowerCounter.getLogs()
            return value, log, has_flower_hu, has_flower, counted_pos

        return 0, None, False, False, False
    
    def c_fan(self):
        curr_deck_counts = self._build_curr_deck_counts()
        self.fanCounter.winner_tiles = curr_deck_counts
        total_fan_value, has_wind, has_zfb, counted_pos = self.fanCounter.count_wind_and_zfb_value()
        has_fan = has_wind or has_zfb

        if not has_wind and not has_zfb:
            value = wind_value
            log = f'無字 +{value}'
            return value, log, has_fan, counted_pos
        
        value = total_fan_value + zfb_value
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
    
    def c_gong_or_4_turtle(self):

        #thirteen waist can technically have 4 turtle
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        if is_special_hu and self.curr_validated_tiles['hu_type'] is not thirteen_waist_hu:
            return 0, None
        
        total_value = 0
        log = []
        gong_tiles = set()
        
        for tile_group in self.curr_validated_tiles['tiles']:
            tile_group = tile_group if isinstance(tile_group, list) else [tile_group]
            if len(tile_group) == 4:
                total_value += gong_value
                log.append(f'槓{tile_group[0]} +{gong_value}')
                gong_tiles.add(tile_group[0])

        for tile, count in self.winner_tiles.items():
            if count == 4 and tile not in gong_tiles and self.door_clear and tile is not joker:
                total_value += dark_four_turtle_value
                log.append(f'暗四歸{tile} +{dark_four_turtle_value}')
            if count == 4 and tile not in gong_tiles and not self.door_clear and tile is not joker:
                total_value += light_four_turtle_value
                log.append(f'明四歸{tile} +{light_four_turtle_value}')

        return total_value, log
    
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

    def _build_curr_deck_counts(self):
        tiles_structure = self.curr_validated_tiles.get('tiles') if isinstance(self.curr_validated_tiles, dict) else None
        if not tiles_structure:
            return self.winner_tiles.copy()

        counts = {}

        for tile_group in tiles_structure:
            tiles = tile_group if isinstance(tile_group, list) else [tile_group]
            for tile in tiles:
                counts[tile] = counts.get(tile, 0) + 1

        return counts

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
    
    def c_lao_shao(self):
        value = 0
        log = []
        suits = {tsm_name[0]: [], tsm_name[1]: [], tsm_name[2]: []}
        
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            numbers = []
            suit = None
            
            for tile in tiles:
                if tile not in zfb_dict and tile not in wind_dict:
                    suit = tile[0]
                    numbers.append(mst_dict[tile])
            
            if len(numbers) >= 3:
                suits[suit].append(sorted(numbers))
        
        # Check each suit for lao shao patterns
        for suit, tile_group in suits.items():
            has_123 = [1, 2, 3] in tile_group
            has_789 = [7, 8, 9] in tile_group
            has_111 = [1, 1, 1] in tile_group
            has_999 = [9, 9, 9] in tile_group
            
            if has_123 and has_789:
                value += lao_shao_value
                log.append(f'老少{suit} +{lao_shao_value}')
            if has_111 and has_999:
                value += lao_shao_value
                log.append(f'老少{suit} +{lao_shao_value}')
        
        return value, log

    def c_ban_gao(self):
        total_value = 0
        log = []

        tested_sets = {}

        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if len(tiles) == 3:
                hashed = tuple(sorted(tiles))
                tested_sets[hashed] = tested_sets.get(hashed, 0) + 1
        
        for _, count in tested_sets.items():
            if count == 2:
                total_value += ban_gao_value
                log.append(f'般高 +{ban_gao_value}')
            elif count == 3:
                total_value += two_ban_gao_value
                log.append(f'兩般高 +{two_ban_gao_value}')
            elif count == 4:
                total_value += three_ban_gao_value
                log.append(f'三般高 +{three_ban_gao_value}')
                
        return total_value, log
    
    def c_sister(self):
        total_value = 0
        log = []
        sisters = {}
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if len(tiles) == 3 and tiles[0] not in zfb_dict and tiles[0] not in wind_dict:
                numbers = set()
                suit = tiles[0][0]
                
                for tile in tiles:
                    tile_number = mst_dict[tile]
                    numbers.add(tile_number)

                if len(numbers) > 1:
                    hashed = tuple(sorted(numbers))
                    temp_list = sisters.get(hashed, set())
                    temp_list.add(suit)
                    sisters[hashed] = temp_list

        for item, value in sisters.items():
            if len(value) == 3:
                total_value += three_sister_value
                log.append(f'三姐妹 +{three_sister_value}')
            if len(value) == 2:
                total_value += sister_value
                log.append(f'姐妹 +{sister_value}')

        return total_value, log

    def c_sister_pong(self):
        total_value = 0
        log = []
        sisters = {}
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if len(tiles) == 3 and tiles[0] not in zfb_dict and tiles[0] not in wind_dict:
                numbers = set()
                suit = tiles[0][0]
                
                for tile in tiles:
                    tile_number = mst_dict[tile]
                    numbers.add(tile_number)

                if len(numbers) == 1:
                    hashed = list(numbers)[0]
                    temp_list = sisters.get(hashed, set())
                    temp_list.add(suit)
                    sisters[hashed] = temp_list
        
        for item, value in sisters.items():
            if len(value) == 3:
                total_value += three_sister_pong_value
                log.append(f'三相逢{item}號牌 +{three_sister_pong_value}')
            if len(value) == 2:
                total_value += sister_pong_value
                log.append(f'兩相逢{item}號牌 +{sister_pong_value}')

        return total_value, log

    def c_dui_dui_or_ping_hu(self):
        type_of_hu = None
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        # Skip duidui/pinghu counting for special hu types
        if is_special_hu:
            return 0, None, type_of_hu
        
        number_of_pongs = 0
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if len(tiles) > 2:
                tracker = set()        
                for tile in tiles:
                    tracker.add(tile)

                if len(tracker) == 1:
                    number_of_pongs += 1

        if number_of_pongs == 5:
            value = dui_dui_hu_value
            log = f'對對胡 +{value}'
            return value, log, 'dui_dui_hu'
        
        if number_of_pongs == 0:
            value = ping_hu_value
            log = f'平胡 +{value}'
            return value, log, 'ping_hu'
        
        return 0, None, type_of_hu
    
    def c_dragons(self):
        number_counter = [False] * 9
        suit_counter = [None] * 9
        valid_tiles = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}]

        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if len(tiles) == 3 and tiles[0] not in zfb_dict and tiles[0] not in wind_dict:
                numbers = set()
                suit = tiles[0][0]

                for tile in tiles:
                    tile_number = mst_dict[tile]
                    numbers.add(tile_number)

                if numbers in valid_tiles:
                    for number in numbers:
                        number_counter[number - 1] = True
                        if suit_counter[number - 1] is None:
                            suit_counter[number - 1] = {suit}
                        else:
                            suit_counter[number - 1].add(suit) 

        if all(number_counter):
            same_house_dragon = False

            for suit in suit_counter[0]:
                suit_in_all = True
                for i in range(1, len(suit_counter)):
                    if suit not in suit_counter[i]:
                        suit_in_all = False
                        break
                if suit_in_all:
                    same_house_dragon = True
                    break

            if same_house_dragon and self.door_clear:
                value = dark_same_dragon_value
                log = f'暗清龍 +{value}'
                return value, log

            if same_house_dragon and not self.door_clear:
                value = light_same_dragon_value
                log = f'明清龍 +{value}'
                return value, log

            if not same_house_dragon and self.door_clear:
                value = dark_mixed_dragon_value
                log = f'暗混龍 +{value}'
                return value, log
            
            if not same_house_dragon and not self.door_clear:
                value = light_mixed_dragon_value
                log = f'明混龍 +{value}'
                return value, log

        return 0, None
    
    def c_less_door(self, has_fan):
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        if is_special_hu:
            return 0, None 
        
        doors = set()
        if has_fan: return 0, None
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            
            if len(tiles) > 2:
                doors.add(tiles[0][0])
        
        if len(doors) > 2: return 0, None

        value = less_one_door_value
        log = f'缺一門 +{less_one_door_value}'

        return value, log
    
    def c_5_doors(self):
        is_special_hu = check_is_special_hu(self.curr_validated_tiles)
        if is_special_hu:
            return 0, None       

        doors = set()
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            if tiles[0] in mst_dict:
                suit = tiles[0][0]
                doors.add(suit)
            if tiles[0] in zfb_dict:
                doors.add('zfb')
            if tiles[0] in wind_dict:
                doors.add('wind')

        if len(doors) == 5:
            value = five_door_value
            log = f'五門齊 +{five_door_value}'
            return value, log

        return 0, None       

    def c_break_waist(self, has_fan):
        hu_type = self.curr_validated_tiles['hu_type']
        if hu_type == thirteen_waist_hu or hu_type == flower_hu or has_fan:
            return 0, None
        
        for item in self.curr_validated_tiles['tiles']:
            tiles = item if isinstance(item, list) else [item]
            for tile in tiles:
                if mst_dict[tile] == 1 or mst_dict[tile] == 9 or tile in zfb_dict or tile in wind_dict:
                    return 0, None
                
        value = break_waist_value
        log = f'斷腰/么 +{break_waist_value}'

        return value, log
