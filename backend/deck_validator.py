from dictionary import *
from helpers import remove_flowers, clean_tiles, remove_and_count_jokers
from types_of_hu import *
from itertools import combinations, product

class DeckValidator:
    def __init__(self, winner_tiles):
        self.winner_tiles = clean_tiles(winner_tiles)
        self.winner_tiles_no_flower = clean_tiles(remove_flowers(winner_tiles))
        self.joker_number, self.winner_tiles_no_joker_no_flower = remove_and_count_jokers(self.winner_tiles_no_flower)
        self.possibleDecks = []

    def full_check(self):
        #Check flower hu
        flower_results = self.flower_hu_check(self.winner_tiles)
        if flower_results:
            self.possibleDecks.append(flower_results)

        #Check there are 17 or more tiles
        if self.card_count(self.winner_tiles_no_flower) < 17 and not flower_results:
            return False
        
        #Check 16bd
        sixteen_bd_results = self.sixteen_bd_check(self.winner_tiles_no_joker_no_flower,self.joker_number)
        if sixteen_bd_results:
            self.possibleDecks.extend(sixteen_bd_results)

        #Check 13 waist
        thirteen_results = self.thirteen_waist_check(self.winner_tiles_no_flower)
        if thirteen_results:
            self.possibleDecks.append(thirteen_results)

        #Check Ligu
        ligu_results = self.ligu_check(self.winner_tiles_no_flower)
        if ligu_results:
            self.possibleDecks.append(ligu_results)
        
        #Check Standard, uses extend because there can be multiple iterations
        standard_results = self.standard_check(self.winner_tiles_no_flower)
        if standard_results:
            self.possibleDecks.extend(standard_results)

        return len(self.possibleDecks) > 0

    def card_count(self, tiles):
        count = 0

        for _, value in tiles.items():
            count += value

        return count
    
    def flower_hu_check(self, tiles):
        flowers = []

        for key in tiles:
            if key in flower_dict:
                flowers.append(key)

        if len(flowers) >= 7:
            return {'hu_type': flower_hu, 'flowers': flowers}

        return []
    
    def ligu_check(self, tiles):
        if (self.card_count(tiles) != 17): return []

        results = {'tiles':[]}
        pairs = 0
        triplets = 0

        for key, value in tiles.items():

            #1 pair
            if value == 2:
                pairs += 1
                results['tiles'].append([key, key])
            
            #2 pairs of the same card
            elif value == 4:
                pairs += 2
                results['tiles'].append([key, key])
                results['tiles'].append([key, key])

            #1 triplet in winning deck
            elif value == 3:
                triplets += 1
                results['tiles'].append([key, key, key])

        results['hu_type'] = ligu_hu
        results['eyes'] = None

        return results if pairs == 7 and triplets == 1 else {}
    
    def sixteen_bd_check(self, tiles, joker_number):

        #Check more than 1 pair
        dap_for_eyes = 0
        eyes = [key for key, value in tiles.items() if value == 2]
        if len(eyes) > 1: return []
        if len(eyes) < 1: dap_for_eyes += 1

        missing_tiles = []
        #Check it has all wind and zfb
        for key in wind_dict:
            if key not in tiles:
                missing_tiles.append(key)
            
        for key in zfb_dict:
            if key not in tiles:
                missing_tiles.append(key)

        #Check at least separated by 3 for m,s,t.
        def sixteenbd_helper(dictionary, suit):
            present = [False] * 10
            present_tiles = set()
            present_numbers = []
            
            for key in tiles:
                if key in dictionary:
                    number = dictionary[key]
                    present[number] = True
                    present_tiles.add(key)
                    present_numbers.append(number)

            #Check that tiles are separated by at least 3
            for i in range(1, 10):
                if present[i]:
                    if (i + 1 <= 9 and present[i + 1]) or (i + 2 <= 9 and present[i + 2]):
                        return False, [], 0
                    
            #No tiles present
            if len(present_tiles) == 0:
                all_combos = combinations(range(1, 10), 3)
                valid_combos = []
                for combo in all_combos:
                    if all(combo[i+1] - combo[i] >= 3 for i in range(len(combo) - 1)):
                        temp = []
                        for number in combo:
                            suited_number = f'{suit}{number}'
                            temp.append(suited_number)
                        valid_combos.append(temp)
                
                return True, valid_combos, 3
            
            #Less than 3 tiles
            if len(present_tiles) < 3:
                present_numbers_sorted = sorted(present_numbers)
                daps_needed = 3 - len(present_tiles)
                valid_combos = []
                
                # Find all possible numbers that can be added
                possible_nums = []
                for num in range(1, 10):
                    if num not in present_numbers:
                        valid = True
                        for temp_num in present_numbers:
                            if abs(num - temp_num) < 3:
                                valid = False
                                break
                        if valid:
                            possible_nums.append(num)
                
                # Generate all combinations of the daps_needed numbers
                for combo in combinations(possible_nums, daps_needed):
                    combined = sorted(present_numbers_sorted + list(combo))
                    if all(combined[i+1] - combined[i] >= 3 for i in range(len(combined) - 1)):
                        temp = []
                        for number in combined:
                            suited_number = f'{suit}{number}'
                            temp.append(suited_number)
                        valid_combos.append(temp)

                return True, valid_combos, daps_needed
            
            #Already have 3 valid tiles
            return True, [sorted(list(present_tiles))], 0

        m_possible, m_combos, m_daps_needed = sixteenbd_helper(m_dict, tsm_name[0])
        t_possible, t_combos, t_daps_needed = sixteenbd_helper(t_dict, tsm_name[1])
        s_possible, s_combos, s_daps_needed = sixteenbd_helper(s_dict, tsm_name[2])
        if not m_possible or not t_possible or not s_possible:
            return []
        
        temp_daps_needed = m_daps_needed + t_daps_needed + s_daps_needed + len(missing_tiles) + dap_for_eyes
        if temp_daps_needed > joker_number:
            return []
        
        curr_present_tiles = []
        for key, value in tiles.items():
            curr_present_tiles.extend([key] * value)

        #Supplementing decks with daps
        close_to_possible_decks = []
        daps_used = 0
        for m_combo, t_combo, s_combo in product(m_combos, t_combos, s_combos):
            temp_deck = curr_present_tiles.copy()

            for tile in missing_tiles:
                temp_deck.append(tile)
                daps_used += 1

            for tile in m_combo:
                if tile in curr_present_tiles:
                    continue
                temp_deck.append(tile)
                daps_used += 1

            for tile in s_combo:
                if tile in curr_present_tiles:
                    continue
                temp_deck.append(tile)
                daps_used += 1

            for tile in t_combo:
                if tile in curr_present_tiles:
                    continue
                temp_deck.append(tile)
                daps_used += 1

            close_to_possible_decks.append(sorted(temp_deck))

        if len(eyes) == 1:
            complete_decks = []
            for item in close_to_possible_decks:
                complete_decks.append({'hu_type': sixteen_bd_hu,'eyes': eyes[0],'tiles': item})
            return complete_decks

        complete_decks = []
        for deck in close_to_possible_decks:
             for tile in deck:
                deck_with_eyes = deck.copy()
                deck_with_eyes.append(tile)
                complete_decks.append({'hu_type': sixteen_bd_hu,'eyes': tile,'tiles': deck_with_eyes})

        return complete_decks            
            
    def thirteen_waist_check(self, tiles):
        tiles_to_remove = []

        #Check it has all wind and zfb
        for key in wind_dict:
            tiles_to_remove.append(key)
            if key not in tiles:
                return []
            
        for key in zfb_dict:
            tiles_to_remove.append(key)
            if key not in tiles:
                return []
            
        def thirteen_helper(prefix, tiles):
            tiles_to_remove.append(f'{prefix}1')
            tiles_to_remove.append(f'{prefix}9')
            return f'{prefix}1' in tiles and f'{prefix}9' in tiles
            
        if not thirteen_helper(tsm_name[0], tiles): return []
        if not thirteen_helper(tsm_name[1], tiles): return []
        if not thirteen_helper(tsm_name[2], tiles): return []
        
        possible_eyes = []

        for key, value in tiles.items():
            if value >= 2:
                temp = tiles.copy()
                temp[key] -= 2
                temp = clean_tiles(temp)
                possible_eyes.append((key, temp))

        for eye, remaining_tiles in possible_eyes:

            for key in tiles_to_remove:
                if key in remaining_tiles and key != eye:
                    remaining_tiles[key] -= 1
            remaining_tiles = clean_tiles(remaining_tiles)

            all_solutions = []
            self.top_down_dfs(remaining_tiles, [], all_solutions)

            if all_solutions:
                # Use the first valid solution and flatten it
                tiles_list = [[eye, eye]]
                tiles_list.extend(all_solutions[0])
                for tile in tiles_to_remove:
                    tiles_list.append([tile])
                return {'hu_type':thirteen_waist_hu, 'eyes': eye, 'tiles': tiles_list}

        return []
    
    def standard_check(self, tiles):        
        #Find all possible eyes
        possible_eyes = []

        for key, value in tiles.items():
            if value >= 2:
                temp = tiles.copy()
                temp[key] -= 2
                temp = clean_tiles(temp)
                possible_eyes.append((key, temp))
        
        results = []
        seen_decks = set()

        for eye, remaining_tiles in possible_eyes:
            all_solutions = []
            self.top_down_dfs(remaining_tiles, [], all_solutions)
            
            for solution in all_solutions:
                complete_sets = [[eye, eye]] + solution
                if len(complete_sets) == 6:
                    sorted_sets = [tuple(sorted(s)) for s in complete_sets]
                    sorted_sets = tuple(sorted(sorted_sets))
                    
                    if sorted_sets not in seen_decks:
                        seen_decks.add(sorted_sets)
                        complete_sets = sorted(complete_sets)
                        results.append({'hu_type': standard_hu, 'eyes': eye, 'tiles': complete_sets})

        return results

    def top_down_dfs(self, tiles, current_sets, all_solutions):
        if not tiles:
            # Found a complete solution, add a copy to all_solutions
            all_solutions.append(current_sets.copy())
            return
        
        #Get a tile from the tiles
        temp = min(tiles.keys())
        
        #1. Try Gong
        if self.test_pong(tiles, temp) and tiles[temp] > 3:
            next_tiles = tiles.copy()
            next_tiles[temp] -= 4
            next_tiles = clean_tiles(next_tiles)

            current_sets.append([temp, temp, temp, temp])
            self.top_down_dfs(next_tiles, current_sets, all_solutions)
            current_sets.pop()  # Backtrack

        #2. Try Pong
        if self.test_pong(tiles, temp):
            next_tiles = tiles.copy()
            next_tiles[temp] -= 3
            next_tiles = clean_tiles(next_tiles)

            current_sets.append([temp, temp, temp])
            self.top_down_dfs(next_tiles, current_sets, all_solutions)
            current_sets.pop()  # Backtrack
        
        #3. Try Shang
        if self.test_shang(tiles, temp):
            next_tiles = tiles.copy()
            suit = temp[0]
            rank = int(temp[1])
            
            next_tiles[temp] -= 1
            next_tiles = clean_tiles(next_tiles)
            
            tile_plus_1 = f'{suit}{rank+1}'
            next_tiles[tile_plus_1] -= 1
            next_tiles = clean_tiles(next_tiles)
            
            tile_plus_2 = f'{suit}{rank+2}'
            next_tiles[tile_plus_2] -= 1
            next_tiles = clean_tiles(next_tiles)
            
            current_sets.append([temp, tile_plus_1, tile_plus_2])
            self.top_down_dfs(next_tiles, current_sets, all_solutions)
            current_sets.pop()  # Backtrack
           
    def test_pong(self, tiles, curr_tile):            
        return tiles[curr_tile] >= 3
    
    def test_shang(self, tiles, curr_tile):
        if curr_tile not in m_dict and curr_tile not in s_dict and curr_tile not in t_dict:
            return False

        suit = curr_tile[0]
        
        number = int(curr_tile[1])
        if number > 7:
            return False
        
        tile_plus_1 = f'{suit}{number+1}'
        tile_plus_2 = f'{suit}{number+2}'
        
        return (curr_tile in tiles and 
                tile_plus_1 in tiles and 
                tile_plus_2 in tiles and 
                tiles[curr_tile] >= 1 and 
                tiles[tile_plus_1] >= 1 and 
                tiles[tile_plus_2] >= 1)
    
    def get_validated_decks(self):
        return self.possibleDecks