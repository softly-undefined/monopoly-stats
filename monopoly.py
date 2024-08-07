import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

#      gy  _g    _g@@g_  @_    *y   _@@@g_ q@Nq_   _g@@g_ qg    *_   _g     
#      @@  @@L  g#`   3g @Mg_   @ _@"   ^@ [F  @L_@F    @ JE     Mg _@`     
#     @F9Lg#3E  @     J# B  0g  @ 0L     @ @Nm#" @F     @ JE      3g@F      
#    _@ ^@@  @_ 0_   _B` @   ^0@N 3&_  _@F $L    3g_  _@F [E  __  _@F       
#    "F  "^  3F  ^MMP"   M     ^"  `"MM"`  ^      `"MM"`  3MMMP"  f^        
#                                                                                                                            
#                   _pMMN  MMM@MMML   g@   PMM@MMMF _pMMN                   
#                   @____     @      @F9L     @     @____                   
#                    ``"0y    @    _@NNMg     0L     ``"0y                  
#                  @g__g0`    @    @^   0y    @L   @g__g0`                  
#                    ``                              ``           
#
# by eric bennett


in_jail = False
jail_turns = 0 #default state
player_pos = 0 #default state
total_turns = 0

monopoly_board = [
    ('GO', 0),
    ('Mediterranean Avenue', 0),
    ('Community Chest 1', 0),
    ('Baltic Avenue', 0),
    ('Income Tax', 0),
    ('Reading Railroad', 0),
    ('Oriental Avenue', 0),
    ('Chance 1', 0),
    ('Vermont Avenue', 0),
    ('Connecticut Avenue', 0),
    ('Jail/Just Visiting', 0),
    ('St. Charles Place', 0),
    ('Electric Company', 0),
    ('States Avenue', 0),
    ('Virginia Avenue', 0),
    ('Pennsylvania Railroad', 0),
    ('St. James Place', 0),
    ('Community Chest 2', 0),
    ('Tennessee Avenue', 0),
    ('New York Avenue', 0),
    ('Free Parking', 0),
    ('Kentucky Avenue', 0),
    ('Chance 2', 0),
    ('Indiana Avenue', 0),
    ('Illinois Avenue', 0),
    ('B&O Railroad', 0),
    ('Atlantic Avenue', 0),
    ('Ventnor Avenue', 0),
    ('Water Works', 0),
    ('Marvin Gardens', 0),
    ('Go to Jail', 0),
    ('Pacific Avenue', 0),
    ('North Carolina Avenue', 0),
    ('Community Chest 3', 0),
    ('Pennsylvania Avenue', 0),
    ('Short Line', 0),
    ('Chance 3', 0),
    ('Park Place', 0),
    ('Luxury Tax', 0),
    ('Boardwalk', 0)
]





def dice_roll():
    roll_1 = random.randint(1, 6)
    roll_2 = random.randint(1, 6)
    roll_total = roll_1 + roll_2
    roll_doubles = False
    if roll_1 == roll_2:
        roll_doubles = True
    return roll_total, roll_doubles

def save_board(filename, monopoly_board):
    data = []

    for space in monopoly_board:
        name, frequency = space
        data.append({'Space': name, 'Frequency': frequency})

    df = pd.DataFrame(data, columns=['Space', 'Frequency'])
    
    df.to_csv(filename, index=False)

def take_turn(player_pos, total_turns, in_jail, consecutive_doubles, jail_turns):
    total_turns += 1

    roll_value, is_double = dice_roll() #roll dice
    if in_jail:
        jail_turns += 1
        if is_double:
            player_pos += roll_value
            in_jail = False
            jail_turns = 0
        else:
            if jail_turns >  3:
                player_pos += roll_value
                in_jail = False
                jail_turns = 0
                #have to pay to get out
            else:
                return player_pos, total_turns, in_jail, consecutive_doubles, jail_turns

        
    else:
        player_pos += roll_value #update player position

    #updates the monopoly_board variable
    board_pos = player_pos % 40

    
    card_draw = random.randint(1, 16)
    if board_pos == 2 or board_pos == 17 or board_pos == 33: #community chests
        if card_draw == 1: #go to GO
            board_pos = 0 #position of GO
        elif card_draw == 6: #go to JAIL
            board_pos = 10 
            in_jail = True
            #need to add jail feature still

    elif board_pos == 7 or board_pos == 22 or board_pos == 36: #chances
        if card_draw == 1: #go to boardwalk
            board_pos = 39
        elif card_draw == 2: #go to GO
            board_pos = 0 #position of GO
        elif card_draw == 3: #go to illinois
            board_pos = 24
        elif card_draw == 4: #go to st charles
            board_pos = 11
        elif card_draw == 11: #go to jail
            board_pos = 10
            in_jail = True
            #need to add jail feature still
        elif card_draw == 14: #go to reading railroad
            board_pos = 5

        #more special cases
        elif card_draw == 10: #go back 3 spaces
            board_pos -= 3 #goes back 3
        elif card_draw == 5 or card_draw == 6: #go to the nearest railroad
            if board_pos == 7: #c1
                board_pos = 15 #pennsylvania
            elif board_pos == 22: #c2
                board_pos = 25 #B&O Railroad
            elif board_pos == 36: #c3
                board_pos = 5 #reading railroad
        elif card_draw == 7: #go to nearest utility
            if board_pos == 7: #c1
                board_pos = 12 #electric company
            elif board_pos == 22: #c2
                board_pos = 28 #water works
            elif board_pos == 36: #c3
                board_pos = 12 #electric company

    elif board_pos == 30: #go to jail
        board_pos = 10
        in_jail = True

    #add to the appropriate landing position
    space_name, frequency = monopoly_board[board_pos]
    monopoly_board[board_pos] = (space_name, frequency + 1)
    player_pos = board_pos

    if is_double: #doubles
        consecutive_doubles += 1
        if consecutive_doubles == 3: #TRIPLE DOUBLES- GO TO JAIL
            board_pos = 10
            in_jail = True
            jail_turns = 0
            space_name, frequency = monopoly_board[board_pos]
            monopoly_board[board_pos] = (space_name, frequency + 1)
            player_pos = board_pos
        else: #double doubles or single doubles
            player_pos, total_turns, is_double, consecutive_doubles, jail_turns = take_turn(player_pos, total_turns, in_jail, consecutive_doubles, jail_turns)
    else:
        consecutive_doubles = 0


    return player_pos, total_turns, is_double, consecutive_doubles, jail_turns




for i in tqdm(range(10000000)):
    player_pos, total_turns, is_double, consecutive_doubles, jail_turns = take_turn(player_pos, total_turns, in_jail, 0, jail_turns)
    
    

save_board("monopoly.csv", monopoly_board)
print(f"total turns: {total_turns}")


