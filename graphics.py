import pygame
import pygame.gfxdraw
from copy import deepcopy
pygame.init()

#aspects of the game window
screenwidth = 800
screenheight = 800
total_red = 12
total_blue = 12

#size of each grid in the board
squarewidth = screenwidth // 8

#default positions of the coins
positions = [0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,0,-1,0,-1,0,0,-1,0,-1,0,-1,0,-1,-1,0,-1,0,-1,0,-1,0]
win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("Checkers")

# updates the board
# MS1: Imports the sprites
black_standard = pygame.image.load('sprites/black-checker/standard.png')
black_King = pygame.image.load('sprites/black-checker/king-me.png')
red_standard = pygame.image.load('sprites/red-checker/standard.png')
red_King = pygame.image.load('sprites/red-checker/king-me.png')

# BLUE = (255,255,240)
# RED = (173,216,230)

BLUE = (255,255,240)
DARK_BLUE = (209, 229, 244)
LIGHTER_BLUE = (229, 249, 264)
RED = (120,144,156)
DARK_RED = (32, 51, 84)
LIGHTER_RED = (52, 71, 104)

def drawsquare(row, column):
    if (7*row + column) % 2 == 1:
        colour = RED
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))
    else:
        colour = BLUE
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))
# f : (row, col) -> {red_standard, black_standard, red_King, black_King}
def drawpieces(row, col):
    factor = 0.9 # factor is adjust the width, height of sprites
    factor1 = 9 # factor1 is to adjust the y-cordinates of centre of sprites
    factor2 = 5 # factor2 is specially for red_King to adjust its centre
    factorx = 1
    index = 8*row + col
    if positions[index] == 1:
        img = pygame.transform.smoothscale(red_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth+factorx, row*squarewidth + factor1))

    elif positions[index] == -1:
        img = pygame.transform.smoothscale(black_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth+factorx, row*squarewidth + factor1))
    
    elif positions[index] == 2:
        img = pygame.transform.smoothscale(red_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth + factor2, row*squarewidth + factor2))
    
    elif positions[index] == -2:
        img = pygame.transform.smoothscale(black_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth, row*squarewidth + factor1))

def highlightSquare(row, col):
    lighter_color = DARK_BLUE if ((7*row + col)%2 == 0) else DARK_RED     
    pygame.draw.rect(win, lighter_color, (col*squarewidth, row*squarewidth, squarewidth, squarewidth))

# draws the legal clear square which a piece can jump to (when)
# you click a piece, it can show you where you can possibly land up
def drawLegalSquare(row, col):
    circle_radius = squarewidth // 6  # Smaller radius for the circle
    darker_color = DARK_BLUE if ((7*row + col) % 2 == 0) else DARK_RED
    center_x = col * squarewidth + squarewidth // 2
    center_y = row * squarewidth + squarewidth // 2
    pygame.gfxdraw.filled_circle(win, center_x, center_y, circle_radius, darker_color)
    

# this indicates all the pieces which would be captured when
# you jump over them
def drawCaptureSquare(row, col): # row and col only
    center_x = col * squarewidth + squarewidth // 2
    center_y = row * squarewidth + squarewidth // 2

    circle_radius = squarewidth // 2.0 # Further increased radius for the hollow circle
    border_width = 5  # Increased width of the border for the hollow circle
    darker_color = DARK_BLUE if ((7*row + col) % 2 == 0) else DARK_RED
    
    # Draw hollow circle which shows the captured square
    pygame.draw.circle(win, darker_color, (center_x, center_y), circle_radius, border_width)

"""
7 indicates the south-west direction
-7 indicates the north-east direction
9 indicates the south-east direction
-9 indicates the north-west direction
You can make sense of these directions by adding them to the index of a cell (row*8+col)
then I find the distance it has from the sides of the board and then find the minimum distance in each direction
then I put the information in the dictionary
"""
legal_coins = dict()
numsToEdges = []
moves = []
for i in range(64):
    numsToEdges.append(dict())
for row in range(8):
    for col in range(8):
        numNorth = row
        numSouth = 7-row
        numWest = col
        numEast = 7 - col
        numsToEdges[row*8 + col] = {
            7: min(numSouth, numWest),
            -7: min(numNorth, numEast),
            9: min(numSouth, numEast),
            -9: min(numNorth, numWest)
        }

def kr(index, dir):
    if numsToEdges[index][dir] < 2:
        return False
    return ((positions[index+dir] == -1 or positions[index+dir] == -2) and positions[index+2*dir]  == 0)
def br(index, dir):
    if numsToEdges[index][dir] < 2:
        return False
    return ((positions[index+dir] == 1 or positions[index+dir] == 2) and positions[index+2*dir]  == 0)

# Gets the square coordinates from mouse click
def getSquareFromClick(pos):
    x, y = pos
    row = y // squarewidth
    col = x // squarewidth
    return row, col

# Draws the complete board
def drawboard():
    k = 0
    key_list = list(legal_coins.keys())
    for i in range(8):
        for j in range(8):
            drawsquare(i,j)
            if 8*i + j in legal_coins:
                highlightSquare(i, j)
            drawpieces(i,j)
    pygame.display.update()

def printPositions():
    for i in range(8):
        for j in range(8):
            piece = positions[i*8+j]
            if piece < 0:
                print(" -1", end = "")
            else:
                print(f"  {piece}", end = "")
        print()

def capture_coin(kill_bit, prev_index, index):
    global total_red
    global total_blue
    x = (index - prev_index) // 2
    if abs(index - prev_index) % 2 == 0:
        if positions[prev_index+x] == 1 or positions[prev_index+x] == 2:
            total_red -= 1
        elif positions[prev_index+x] == -1 or positions[prev_index+x] == -2:
            total_blue -= 1
        if total_red == 0:
            print("Blue wins")
        elif total_blue == 0:
            print("Red wins")
    if kill_bit:
        positions[prev_index+x] = 0
        positions[index] = deepcopy(positions[prev_index])
        positions[prev_index] = 0
    else:
        positions[index] = deepcopy(positions[prev_index])
        positions[prev_index] = 0
    row = index//8
    if row == 0 and (positions[index] == -1):
        positions[index] = -2
    elif row == 7 and (positions[index] == 1):
        positions[index] = 2
    drawboard()
        
def display_kill_moves(row, col, moves):
    set_positions = []
    index = 8*row + col
    for move in moves:
        Index = index + move
        row_f = Index // 8
        col_f = Index%8
        drawCaptureSquare(row_f, col_f)
        Index += move
        set_positions.append(Index)
        row_f = Index // 8
        col_f = Index%8
        drawLegalSquare(row_f,col_f)
    pygame.display.update()    
    return set_positions

def display_normal_moves(row, col, moves):
    set_positions = []
    index = 8*row + col
    for move in moves:
        Index = index + move
        set_positions.append(Index)
        row_f = Index // 8
        col_f = Index%8
        drawLegalSquare(row_f,col_f)
    pygame.display.update()
    return set_positions

def getkillmoves(index):
    dir = []
    coin = positions[index]
    if coin == 1:
        dir = [7,9]
    if coin == 2:
        dir = [-9,-7,7,9]
    for i in dir:
        if kr(index, i):
            moves.append(i)
    dir = []
    if coin == -1:
        dir = [-7,-9]
    if coin == -2:
        dir = [-9,-7,7,9]
    for i in dir:
        if br(index, i):
            moves.append(i)

def getnormalmoves(index):
    dir = []
    coin = positions[index]
    if coin==1:
        dir = [7,9]
    if coin == 2 or coin == -2:
        dir = [-9,-7,7,9]
    if coin == -1:
        dir = [-7,-9]
    for i in dir:
        if (numsToEdges[index][i] >= 1) and (positions[index+i] == 0):
            moves.append(i)

def getlegalcoins(positions, red_turn, prev_row, prev_col):
    legal_coins.clear()
    if not prev_row == -1:
        index = prev_row*8 + prev_col
        coins = [-2,-1,1,2]
        for i in coins:
            if positions[index] == i:
                getkillmoves(index)
                if len(moves):
                    legal_coins[index] = deepcopy(moves)
                    moves.clear()
                    return legal_coins, True
        return legal_coins, False 
    else:
        kill_bit = False 
        if red_turn:
            coins = [1,2]
        else:
            coins = [-1,-2]
        for index in range(64):
                if kill_bit:
                    for i in coins:
                        if positions[index] == i:
                            getkillmoves(index)
                            if len(moves):
                                legal_coins[index] = deepcopy(moves)
                                moves.clear()                  
                else:
                    for i in coins:
                        if positions[index] == i:
                            getkillmoves(index)
                            if len(moves):
                                legal_coins.clear()
                                legal_coins[index] = deepcopy(moves)
                                kill_bit = True
                                moves.clear()
                                break
                            getnormalmoves(index)
                            if len(moves):
                                legal_coins[index] = deepcopy(moves)
                                moves.clear()
        return legal_coins, kill_bit
                            





            