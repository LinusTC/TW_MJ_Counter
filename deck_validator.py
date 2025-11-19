from dictionary import *
from helpers import remove_flowers
class DeckValidator:
    def __init__(self, winner_tiles):
        self.winner_tiles = winner_tiles
        self.winner_tiles_no_flower = remove_flowers(winner_tiles)
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
        return False