from dictionary import dir_dict, f_dict, w_dict, t_dict, s_dict

def count_compass(winner_seat, curr_circle, winner_cards):
    count = 0
    compass_eyes = False
    
    #Counts compass
    for key in winner_cards:
        if key not in dir_dict:
            continue
        else:
            if winner_cards[key] >= 3:
                count += 1
            if winner_cards[key] == 2:
                compass_eyes = True

    #Counts curr circle
    if winner_cards[curr_circle] == 3:
        count += 1

    #Counts seat position
    if winner_cards[winner_seat] == 3:
        count += 1

    #No compass cards, NEED TO CHANGE
    if count == 0: 
        return 1 if not compass_eyes else 0
    
    return count

if __name__ == "__main__":
    test = {'east' : 3, 'west': 3}
    winner_seat = 'east'
    curr_circle = 'west'

    print(count_compass(winner_seat, curr_circle, test))