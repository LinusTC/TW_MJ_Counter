from dictionary import *
from helpers import remove_flowers
class DeckValidator:
    def __init__(self, winner_cards):
        self.winner_cards = winner_cards
        self.winner_cards_no_flower = remove_flowers(winner_cards)
        self.possibleDecks = []

    def standard_check(self):
        #Check there are 17 or more cards
        if self.card_count(self.winner_cards_no_flower) < 17:
            return False
        
        #Check Ligu
        if self.ligu_check(self.winner_cards_no_flower):
            self.possibleDecks.append(['ligu', self.winner_cards])
            return True
        
        #Check 16bd
        if self.sixteen_bd_check(self.winner_cards_no_flower):
            self.possibleDecks.append(['16bd', self.winner_cards])
            return True
        
        #Check 13 waist
        if self.thirteen_waist_check(self.winner_cards_no_flower):
            self.possibleDecks.append(['13waist', self.winner_cards])
            return True

        return False

    def card_count(self, cards):
        count = 0

        for _, value in cards.items():
            count += value

        return count
    
    def ligu_check(self, cards):
        
        pairs = 0
        triplets = 0

        for _, value in cards.items():

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
    
    def sixteen_bd_check(self, cards):

        #Check it has all compass and zfb
        for key in compass_dict:
            if not cards[key]:
                return False
            
        for key in zfb_dict:
            if not cards[key]:
                return False

        cards = cards.copy()
            
        return True
    
    def thirteen_waist_check(self, cards):
        return None
    
