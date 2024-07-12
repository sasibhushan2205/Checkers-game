import pygame
import numpy as np
from graphics import *

run = True # for the while loop
red_turn = True
turnon = True
kill_bit = False
setmode = False
kill_streak = False
coins_moves = []
red_coins_moves = []
blue_coins_moves = []
set_positions = []
red_set_positions = []
blue_set_positions = []
prev_col_g, prev_row_g = -1, -1
prev_row, prev_col = -1, -1
idle_kill_count = 0
winner = False
turnon = True
while run:
    # If you want to quit in middle, just close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if idle_kill_count == 40:
            winner = False
            run = False
        if red_turn and turnon:
            idle_kill_count+=1
            red_coins_moves, kill_bit = getlegalcoins(positions, True, prev_row_g, prev_col_g)
            if kill_bit:
                idle_kill_count = 0
            if prev_row_g == -1 and not (red_coins_moves):
                run = False
                winner = False
            turnon = False
            drawboard()
            if not len(red_coins_moves) :
                prev_row_g = -1
                red_turn = False
                turnon = True
        elif not red_turn and turnon:
            idle_kill_count+=1
            blue_coins_moves, kill_bit = getlegalcoins(positions, False, prev_row_g, prev_col_g)
            if kill_bit:
                idle_kill_count = 0
            if prev_row_g == -1 and not (blue_coins_moves):
                run = False
                winner = True
            turnon = False
            drawboard()
            if not len(blue_coins_moves):
                prev_row_g = -1
                red_turn = True
                turnon = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:
                clicked_pos = getSquareFromClick(pygame.mouse.get_pos())
                row, col = clicked_pos
            index = 8*row + col 
            if setmode:
                if red_turn:
                    set_positions = red_set_positions
                else:
                    set_positions = blue_set_positions
                for i in set_positions:
                    if i == index:
                        prev_index = 8*prev_row + prev_col
                        capture_coin(kill_bit, prev_index, index)
                        setmode = False
                        kill_streak = kill_bit
                        if kill_streak:
                            prev_row_g = row
                            prev_col_g = col
                            turnon = True
                        else: 
                            prev_row_g = -1
                            if red_turn:
                                red_turn = False
                            else:
                                red_turn = True
                            turnon = True
                        break
                
                if setmode:
                    set_positions.clear()
                    drawboard()
                else:
                    continue

            moves = []
            if red_turn:
                coins_moves = red_coins_moves
            else:
                coins_moves = blue_coins_moves
            for obj in coins_moves:
                if obj == index:
                    moves = deepcopy(coins_moves[obj])
                    break
            if len(moves):
                if kill_bit:
                    if red_turn: 
                        red_set_positions = display_kill_moves(row, col, moves)
                    else:
                        blue_set_positions = display_kill_moves(row, col, moves)
                else:
                    if red_turn:
                        red_set_positions = display_normal_moves(row, col, moves)
                    else:
                        blue_set_positions = display_normal_moves(row, col, moves)
                prev_row = row
                prev_col = col
                setmode = True
            else:
                prev_row = -1
                prev_col = -1
                setmode = False
        
                    
            
                        
            

                
                