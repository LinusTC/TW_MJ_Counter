from dictionary import *
from helpers import remove_flowers, clean_tiles
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
        if self.flower_hu_check(self.winner_tiles):
            self.possibleDecks.append(['flower hu', self.winner_tiles])
            return True
        
        #Check Ligu
        if self.ligu_check(self.winner_tiles_no_flower):
            self.possibleDecks.append(['ligu', self.winner_tiles])
            return True
        
        #Check 16bd
        if self.sixteen_bd_check(self.winner_tiles_no_flower):
            self.possibleDecks.append(['16bd', self.winner_tiles])
            return True
        
        #Check 13 waist
        if self.thirteen_waist_check(self.winner_tiles_no_flower):
            self.possibleDecks.append(['13waist', self.winner_tiles])
            return True
        
        #Check Standard, already adds to possible decks on its own
        if self.standard_check(self.winner_tiles_no_flower):
            return True

        return False

    def card_count(self, tiles):
        count = 0

        for _, value in tiles.items():
            count += value

        return count
    
    def flower_hu_check(self, tiles):
        flower_count = 0

        for key in tiles:
            if key in flower_dict:
                flower_count += 1

        if flower_count > 6:
            return True
        
        return False
    
    def ligu_check(self, tiles):
        
        pairs = 0
        triplets = 0

        for _, value in tiles.items():

            #1 pair
            if value == 2:
                pairs += 1
            
            #2 pairs of the same card
            elif value == 4:
                pairs += 2

            #1 triplet in winning deck
            elif value == 3:
                triplets += 1

        return True if pairs == 7 and triplets == 1 else False
    
    def sixteen_bd_check(self, tiles):

        #Check it has all compass and zfb
        for key in compass_dict:
            if key not in tiles:
                return False
            
        for key in zfb_dict:
            if key not in tiles:
                return False

        #Check at least separated by 3 for m,s,t.
        def sixteenbd_helper(dictionary):
            temp = 0
            present = [False] * 10
            for key in tiles:
                if key in dictionary:
                    present[dictionary[key]] = True
                    temp += 1

            #Check that there are at least 3 tiles
            if temp < 3:
                return False
            
            for i in range(1, 10):
                if present[i]:
                    if (i + 1 <= 9 and present[i + 1]) or (i + 2 <= 9 and present[i + 2]):
                        return False
                    
            return True
                    
        if not sixteenbd_helper(m_dict): return False

        if not sixteenbd_helper(s_dict): return False
        
        if not sixteenbd_helper(t_dict): return False
        
        #Checks there is only 1 pair of eyes
        temp = 0
        for key, value in tiles.items():
            if value == 2:
                temp += 1
                
        return True if temp == 1 else False
    
    def thirteen_waist_check(self, tiles):
        #Check it has all compass and zfb
        for key in compass_dict:
            if key not in tiles:
                return False
            
        for key in zfb_dict:
            if key not in tiles:
                return False
        return None
    
    def standard_check(self, tiles):        
        #Find all possible eyes
        possible_eyes = []

        for key, value in tiles.items():
            if value >= 2:
                temp = tiles.copy()
                temp[key] -= 2
                tiles = clean_tiles(tiles)
                possible_eyes.append((key, temp))
        
        found_valid = False

        for eye, remaining_tiles in possible_eyes:
            complete_sets = []
            memo = {}
            if self.top_down_dfs(remaining_tiles, memo, complete_sets):
                if len(complete_sets) == 5:
                    self.possibleDecks.append(['standard', {'eye': eye, 'tiles': complete_sets}])
                    found_valid = True

        return found_valid

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