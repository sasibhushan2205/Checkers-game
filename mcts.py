import numpy as np
from copy import deepcopy

# AKSHATH, VERY IMP -- Done
# MIGHT NEED TO CONSIDER KEEPING OPPONENT AS -1, -2 instead of 1, 3 to make it easier to flip state -- Done
class Checkers:
    global numsToEdges
    global moves
    moves = []
    numsToEdges = []
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

    def __init__(self):
        pass
    
    def get_initial_state(self):
        return [0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,0,-1,0,-1,0,0,-1,0,-1,0,-1,0,-1,-1,0,-1,0,-1,0,-1,0]
   
    # action is defined as (initial_index, direction, kill_bool)
    def get_next_state(self, state, action, player): # If reaches last row, make it 2 instead of 1 # AKSHATH
        initial_index, direction, kill_bool = action

        state[initial_index+((kill_bool+1)*direction)] = player
        if (initial_index+((kill_bool+1)*direction))//8 == 7 or (initial_index+((kill_bool+1)*direction))//8 == 0:
            state[initial_index+((kill_bool+1)*direction)] *= 2
        # AKSHATH | kING IDENTIFIER
        if kill_bool:
            state[initial_index+direction] = 0 # needs t0 be changed

        return state
    
    def kr(self, state, index, dir):
        if numsToEdges[index][dir] < 2:
            return False
        return ((state[index+dir] == -1 or state[index+dir] == -2) and state[index+2*dir]  == 0)

    def br(self, state, index, dir):
        if numsToEdges[index][dir] < 2:
            return False
        return ((state[index+dir] == 1 or state[index+dir] == 2) and state[index+2*dir]  == 0)

    def getnormalmoves(self, state, index):
        dir = []
        coin = state[index]
        if coin==1:
            dir = [7,9]
        if coin == 2 or coin == -2:
            dir = [-9,-7,7,9]
        if coin == -1:
            dir = [-7,-9]
        for i in dir:
            if (numsToEdges[index][i] >= 1) and (state[index+i] == 0):
                moves.append(i)
    
    def getkillmoves(self, state, index):
        dir = []
        coin = state[index]
        if coin == 1:
            dir = [7,9]
        if coin == 2:
            dir = [-9,-7,7,9]
        for i in dir:
            if self.kr(self, state, index, i):
                moves.append(i)
        dir = []
        if coin == -1:
            dir = [-7,-9]
        if coin == -2:
            dir = [-9,-7,7,9]
        for i in dir:
            if self.br(self, state, index, i):
                moves.append(i)
    
    def get_valid_moves(self, state, args):
        legal_actions = []
        if not args['prev_index'] == -1:
            index = args['prev_index']
            coins = [1,2]
            for i in coins:
                if state[index] == i:
                    self.getkillmoves(state, index)
                    if len(moves):
                        for i in moves:
                            legal_actions.append([index, i, True])
                        moves.clear()
                        return legal_actions
            return legal_actions
        else:
            coins = [1, 2]
            kill_bit = False
            for index in range(64):
                if kill_bit:
                    for i in coins:
                        if state[index] == i:
                            self.getkillmoves(state, index)
                            if len(moves):
                                for j in moves:
                                    legal_actions.append([index, j, True])
                                moves.clear()
                else:
                    for i in coins:
                        if state[index] == i:
                            self.getkillmoves(state, index)
                            if len(moves):
                                legal_actions.clear()
                                for j in moves:
                                    legal_actions.append([index, j, True])
                                kill_bit = True
                                moves.clear()
                                break
                            self.getnormalmoves(state, index)
                            if len(moves):
                                for j in moves:
                                    legal_actions.append([index, j, True])
                                moves.clear()
            return legal_actions
        # AKSHATH - Done

    def check_win(self, state, action): # after doing the action, returns True if player has won and False if player has not won (yet, this might be in the middle of the game or the opponent has won)
        if action == None:
            return False # Root node has None as action so returns False
        
        # Below code is the same as get_next_state
        initial_index, direction, kill_bool = action
        # state[initial_index + (kill_bool+1)*direction]

        # if player: # AKSHATH | REDUNDANT IF PLAYER IS FIXED
        #     opponent = 0
        # else:
        #     opponent = 1
        opponent = -1
        if opponent in state:
            return False # May ignore conditions where there is no legal moves while opponent still having pieces (that is technically a win | Also ignores the draw condition)
        opponent = -2
        if opponent in state:
            return False
            # AKSHATH
        return True

    def isDraw(self, state, action, args):
        # AKSHATH
        # Store the draw condition
        # I guess we need to store some args along with the state as well such that the args store the number of moves since any killing (40 limit in our case)
        # Decide whether to propogate args grouped with state or args variables separately
        pass


    def get_value_and_terminated(self, state, action, args):
        if self.check_win(state, action):
            return 1, True # True means that this is a terminal value and 1 means the guy who played the move (can be opponent, can be the player) has won.
        if self.isDraw(state, action, args):
            return 0, True # 0 because no one has won (Would work only if we keep calculation as 1 for player and -1 for opponent) # AKSHATH
        return 0, False # No one has won but also the game has not terminated yet

    def get_opponent(self, player):
        if player:
            opponent = 0
        else:
            opponent = 1
        return opponent
    
    def get_opponent_value(self, value):
        -value # AKSHATH (I maybe don't think the function would work for our case as we are using 0, 1 instead of -1, 1, So look into it and see if we need to change this )

    def change_perspective(self, state, player): # THIS FUNCTION IS COMPUTATIONALLY HEAVY, WOULD BE EASIER IF WE COULD JUST MULTIPLY BY -1 TO FLIP THE PLAYERS
        if player:
            opponent = 0
        else:
            opponent = 1
        state[state == opponent] == -4 # temporarily changing opponent values
        state[(state != -1) and (state!=-4) and (state%2 == player)] = (state//2)+opponent # Changing player val;'0P"ues to opponent values
        state[state == -4] = player # Changing the earlier stored oppoenent values to player




class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken

        self.children = [] # all the children of this node | An array of Node objects
        self.expandable_moves = game.get_valid_moves(state) # all the valid moves I can take from this state
 
        self.visit_count = 0 # number of times the node is visited
        self.value_sum = 0 # number of wins when I take this node

    def fullyExpanded(self): # to check whether all the moves in the node has been visited # AKSHATH
        pass

    def select(self): # select down selection
        # calculated ucb score for each child and select the node with the highest UCB score
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child) # 
            if ucb> best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        q_value = 1 - (child.value_sum / child.visit_count) # child.value_sum is the value perceived by the child (child is the opponent player!)
        return  q_value + self.args['c']*np.sqrt(np.log((self.visit_count/child.visit_count)))
    
    def expand(self):
        action = np.random.choice((self.expandable_moves))
        self.expandable_moves.remove(action)

        child_state = deepcopy(self.state) # AKSHATH # I want to child to copy parents state, I am not sure whether this method leads to memory leaks. Author used self.state.copy() # 
        child_state = self.game.get_next_state(child_state, action, 1) # AKSHATH 
        # VERY IMPORTANT
        # The MCTS tree always thinks that it is plyaing for player 1 but what we do is we just flip the players in the child state. 
        # Apparently this makes things easier, but we might think of some other implementation, for now I am implementing this change in perspective

        child = Node(self.game, self.args, child_state, self, action) # Creation of the child node
        # AKSHATH | CHANGE PERSPECTIVE FUNCTION
        self.game.get_opponent(self, child)
        child_state = self.game.change_perspective(child_state, player = -1) # WE DEFINITELY NEED TO CHANGE THE ALL VALUES
        self.children.append(child)
        return child

class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state):
        root = Node(self.game, self.args, state) # initialises root node
        for search in range(self.args['num_searches']):
            node = root
            # SELECTION
            # keep selecting all the nodes
            while node.fullyExpanded():
                node = node.select()
            # now we have reached the leaf node            
            value, termination = self.game.get_value_and_termination(node.state, node.action_taken) # determines if the leaf node is terminal node or not | Action taken is done by the parent for a node (so action of the opponent of the node)
            value = self.game.get_opponent_value(value)
            
            if not termination: # So we have to expand and simulate from this node
                node = node.expand() # Get the next child node to be expanded

            # EXPANSION
            # SIMULATION
            # BACKPROPOGATION

        # return visit_counts
