from dictionary import *

def remove_flowers(cards):
    cards_copy = cards.copy()
    keys_to_delete = []
    for key in cards_copy:
        if key in flower_dict:
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del cards_copy[key]

    return cards_copy