from dictionary import *
from types_of_hu import *

def remove_flowers(tiles):
    tiles_copy = tiles.copy()
    keys_to_delete = []
    for key in tiles_copy:
        if key in flower_dict:
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del tiles_copy[key]

    return tiles_copy

def clean_tiles(tiles):
    return {key: value for key, value in tiles.items() if value > 0}

def check_is_special_hu(validated_deck):
    hu_type = validated_deck['hu_type']
    is_special_hu = hu_type in (sixteen_bd_hu, thirteen_waist_hu, ligu_hu, flower_hu)
    return is_special_hu