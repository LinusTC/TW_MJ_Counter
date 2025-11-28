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

def find_tiles_that_complete_set(incomplete_set):
    if len(incomplete_set) > 2: 
        return {}
    
    #Eyes 
    if len(incomplete_set) == 1:
        return {'complete_type' : eyes,'tiles': [incomplete_set[0]]}

    #Pong
    if incomplete_set[0] == incomplete_set[1]:
        return {'complete_type' : pong, 'tiles': [incomplete_set[0]]}

    #Shang 
    if incomplete_set[0] != incomplete_set[1]:  
        suit = incomplete_set[0][0]
        incomplete_set = sorted(incomplete_set, key=lambda x: mst_dict[x])
        num1 = mst_dict[incomplete_set[0]]
        num2 = mst_dict[incomplete_set[1]]
    
        possible = []
        
        if num1 + 1 == num2:
            if num1 - 1 > 0:
                possible.append(f'{suit}{num1 - 1}')
            if num2 + 1 < 10:
                possible.append(f'{suit}{num2 + 1}')
            return {'complete_type' : shang, 'tiles': possible}
        else:
            return {'complete_type' : shang, 'tiles': [f'{suit}{num1 + 1}']}