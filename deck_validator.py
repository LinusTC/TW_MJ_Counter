from dictionary import *
from helpers import remove_flowers, clean_tiles
from types_of_hu import *
class DeckValidator:
    def __init__(self, winner_tiles):
        self.winner_tiles = clean_tiles(winner_tiles)
        self.winner_tiles_no_flower = clean_tiles(remove_flowers(winner_tiles))
        self.possibleDecks = []

    def full_check(self):
        #Check there are 17 or more tiles
        if self.card_count(self.winner_tiles_no_flower) < 17:
            return False
        
        #Check flower hu
        flower_results = self.flower_hu_check(self.winner_tiles)
        if flower_results:
            self.possibleDecks.append(flower_results)
            return True
        
        #Check Ligu
        ligu_results = self.ligu_check(self.winner_tiles_no_flower)
        if ligu_results:
            self.possibleDecks.append(ligu_results)
            return True
        
        #Check 16bd
        sixteen_bd_results = self.sixteen_bd_check(self.winner_tiles_no_flower)
        if sixteen_bd_results:
            self.possibleDecks.append(sixteen_bd_results)
            return True
        
        #Check 13 waist
        thirteen_results = self.thirteen_waist_check(self.winner_tiles_no_flower)
        if thirteen_results:
            self.possibleDecks.append(thirteen_results)
            return True
        
        #Check Standard, uses extend because there can be multiple iterations
        standard_results = self.standard_check(self.winner_tiles_no_flower)
        if standard_results:
            self.possibleDecks.extend(standard_results)
            return True

        return False

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

        results = {'pairs':[], 'triple':[]}

        for key, value in tiles.items():

            #1 pair
            if value == 2:
                results['pairs'].append(f'{key}, {key}')
            
            #2 pairs of the same card
            elif value == 4:
                results['pairs'].append(f'{key}, {key}')
                results['pairs'].append(f'{key}, {key}')

            #1 triplet in winning deck
            elif value == 3:
                results['triple'].append(f'{key}, {key}, {key}')

        results['hu_type'] = ligu_hu
        return [results] if len(results['pairs']) == 7 and len(results['triple']) == 1 else []
    
    def sixteen_bd_check(self, tiles):
        #Check it has all wind and zfb
        for key in wind_dict:
            if key not in tiles:
                return []
            
        for key in zfb_dict:
            if key not in tiles:
                return []

        #Check at least separated by 3 for m,s,t.
        def sixteenbd_helper(dictionary):
            temp = 0
            present = [False] * 10
            for key in tiles:
                if key in dictionary:
                    present[dictionary[key]] = True
                    temp += 1

            # Check that there are at least 3 tiles
            if temp < 3:
                return False

            for i in range(1, 10):
                if present[i]:
                    if (i + 1 <= 9 and present[i + 1]) or (i + 2 <= 9 and present[i + 2]):
                        return False

            return True

        if not sixteenbd_helper(m_dict):return []
        if not sixteenbd_helper(s_dict):return []
        if not sixteenbd_helper(t_dict):return []

        #Find pair of eyes
        eyes = [key for key, value in tiles.items() if value == 2]
        if len(eyes) != 1: return None

        all_tiles = []
        for key, value in tiles.items():
            all_tiles.extend([key] * value)

        return {'hu_type': sixteen_bd_hu,'eyes': eyes[0],'tiles': all_tiles}
    
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
            
        if not thirteen_helper('t', tiles): return []
        if not thirteen_helper('s', tiles): return []
        if not thirteen_helper('m', tiles): return []
        
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

            complete_sets = []
            memo = {}

            if self.top_down_dfs(remaining_tiles, memo, complete_sets):
                tiles_list = complete_sets + tiles_to_remove.copy()
                tiles_list.append(eye)
                return {'hu_type':thirteen_waist_hu, 'eye': eye, 'tiles': tiles_list}

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

        for eye, remaining_tiles in possible_eyes:
            complete_sets = []
            complete_sets.append(f'{eye}, {eye}')
            memo = {}
            if self.top_down_dfs(remaining_tiles, memo, complete_sets):
                if len(complete_sets) == 6:
                    results.append({'hu_type': standard_hu, 'eye': eye, 'tiles': complete_sets})

        return results

    def top_down_dfs(self, tiles, memo, complete_sets):
        if not tiles:
            return True
        
        #Convert tuple so that it can be stored in dictionary
        sorted_tiles = tuple(sorted(tiles.items()))
        if sorted_tiles in memo:
            return memo[sorted_tiles]
        
        #Get a tile from the tiles
        temp = min(tiles.keys())
        
        #1. Try Gong
        if self.test_pong(tiles, temp) and tiles[temp] > 3:
            next_tiles = tiles.copy()
            next_tiles[temp] -= 4
            next_tiles = clean_tiles(next_tiles)

            if self.top_down_dfs(next_tiles, memo, complete_sets):
                memo[sorted_tiles] = True
                complete_sets.append(f'{temp}, {temp}, {temp}, {temp}')
                return True

        #2. Try Pong
        if self.test_pong(tiles, temp):
            next_tiles = tiles.copy()
            next_tiles[temp] -= 3
            next_tiles = clean_tiles(next_tiles)

            if self.top_down_dfs(next_tiles, memo, complete_sets):
                memo[sorted_tiles] = True
                complete_sets.append(f'{temp}, {temp}, {temp}')
                return True
        
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
            
            if self.top_down_dfs(next_tiles, memo, complete_sets):
                memo[sorted_tiles] = True
                complete_sets.append(f'{temp}, {suit}{rank+1}, {suit}{rank+2}')
                return True
        
        memo[sorted_tiles] = False
        return False
           
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