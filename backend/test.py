from dictionary import *
from deck_validator import DeckValidator
from full_counter import FullCounter

if __name__ == "__main__":
    fa_test = {'f1': 1, "ff1": 1, 'f2': 1, 'ff2': 1, "f3": 1, 'ff3': 1, 'f4':1, 'ff4':1}
    sixteenbd_test = {'m1': 1, 'm5': 1, 'm9': 1, 's1': 1, 's4': 1, 's7': 1, 't1': 1, 't6': 1, 't9': 1, 'east': 1, 'south': 1, 'west': 2, 'north': 1, 'zhong': 1, 'fa': 1, 'bai':1}
    Thirteen_waist_test = {'m1': 1, 'm9':1, 's1': 1, 's9':1, 't1': 1, 't7':1, 't8':1, 't9':3, 'east': 1, 'south': 1, 'west': 1, 'north': 1, 'zhong': 1, 'fa': 1, 'bai':1}
    ligu_test = {'m1': 4, 'm5': 4, 't1': 4, 'zhong': 2, 'bai': 3}
    standard_test = {'m2':1, 'm3':1, 'f2':1, 'f1': 1, 'ff4': 1, 'm4': 1, 's5': 3, 's2':1, 's3': 1, 's4': 1, 't4': 2, 't2': 2, 't3':2, 't8':2}
    joker_test = {'joker':2, 'fa': 0, 'm7': 2, 'm5': 2, 't1': 4, 'zhong': 2, 'bai': 3,}

    winner_seat = 2
    curr_wind = 'west'

    # All test cases
    tests = {
        'joker_test': joker_test
    }
    
    # Run all tests
    for test_name, test_tiles in tests.items():
        print(f'\n{"="*60}')
        print(f'Testing: {test_name}')
        print(f'{"="*60}')
        
        deck_validator = DeckValidator(test_tiles)
        has_valid_deck = deck_validator.full_check()
        print(f'Has valid decks: {has_valid_deck}')
        
        full_counter = FullCounter(test_tiles, winner_seat, curr_wind, 'm1', True, True, 0, 1)
        count, logs, winning_deck, winning_deck_organized = full_counter.full_count()
        print(f'Count: {count}')
        print(f'Logs: {logs}')
        print(f'Winning deck: {winning_deck}')
        print(f'Winning deck_organized: {winning_deck_organized}')

        print(f'{"="*60}\n')