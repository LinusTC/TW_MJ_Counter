from dictionary import *
from fan_counter import FanCounter
from flower_counter import FlowerCounter
from deck_validator import DeckValidator

if __name__ == "__main__":
    fa_test = {'f1': 1, "ff1": 1, 'f2': 1, 'ff2': 1, "f3": 1, 'ff3': 1, 'f4':1, 'ff4':1, 'west' : 4, 'east': 4, 'fa': 2, 'bai': 2, 'north': 2, 'south': 3}
    sixteenbd_test = {'m1': 1, 'm5': 1, 'm9': 1, 's1': 1, 's4': 1, 's7': 1, 't1': 1, 't6': 1, 't9': 1, 'east': 1, 'south': 1, 'west': 2, 'north': 1, 'zhong': 1, 'fa': 1, 'bai':1}
    Thirteen_waist_test = {'m1': 1, 'm9':1, 's1': 1, 's9':1, 't1': 1, 't7':1, 't8':1, 't9':3, 'east': 1, 'south': 1, 'west': 1, 'north': 1, 'zhong': 1, 'fa': 1, 'bai':1}
    ligu_test = {'m1': 2, 'm5': 2, 'm9': 2, 's1': 2, 's4': 2, 's7': 2, 't1': 2, 't6': 3}
    standard_test = {'m1': 3, 'm2':2, 'm3':2, 'm4': 2, 's1':2, "t3":4, 'east': 4}

    winner_seat = 2
    curr_circle = 'west'

    deck_validator = DeckValidator(standard_test)
    has_valid_deck = deck_validator.full_check()
    print(f'Has valid decks: {has_valid_deck}')
    for item in deck_validator.possibleDecks:
        print(item)