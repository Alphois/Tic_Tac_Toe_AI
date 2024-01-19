"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = 0
    os = 0
    if (terminal(board)):
        return -1;
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                xs+=1
            elif board[i][j] == O:
                os+=1
    if xs+os == 9:
        return -1
    if xs == os:
        return X
    else: 
        return O
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board) or action == None:
        return board
    
    turn = player(board)
    # turn = either "X" or "O"
    board_i=copy.deepcopy(board);
    board_i[action[0]][action[1]] = turn
    return board_i
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = utility(board)
    if winner == 1:
        return "X"
    elif winner ==-1:
        return "O"
    else:
        return None
    


def terminal(board):    
    """
    Returns True if game is over, False otherwise.
    """
    won_or_not = utility(board)
    if won_or_not == 1 or won_or_not == -1 or all(board[row][j]!= EMPTY  for row in range(len(board)) for j in range(len(board[row]))):
    # if every row is filled in or utility is -1 or utility is 1
        return True
    return False

directions_coll = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1, -1), (0,-1), (1,-1)]
# first is right, next is diagonally down right, next is down, next is diagonally down left, then left, diagonally upper left, up, top right
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # def dfs(direction, index, player, count):   
    #     x = index[0]
    #     y = index[1]
    #     if x>=0 and x<3 and y<3 and y>=0:
    #         if board[x][y]== player:
    #             count+=1
    #             if count==2:
    #                 count = 0
    #                 return player
    #         dfs(direction, (index[0] + direction[0], index[1]+ direction[1]), player, count)
    #     else:
    #         return None
    # for i in range(len(board)):
    #     for j in range(len(board[i])):
    #         if board[i][j] != EMPTY:
    #             for z in directions_coll:
    #                 player_win = dfs(z, (i+z[0], j + z[1]), board[i][j], 0)
    #                 if player_win is not None:
    #                     if player_win == X:
    #                         return 1
    #                     if player_win== O:
    #                         return -1              
    # return 0
    # swap to iterative, this is too inefficient

    for player in [X, O]:
        for i in range(3):
            # Check rows and columns
            if board[i] == [player] * 3 or [row[i] for row in board] == [player] * 3:
                return 1 if player == X else -1
        # Check diagonals
        if [board[i][i] for i in range(3)] == [player] * 3 or [board[i][2 - i] for i in range(3)] == [player] * 3:
            return 1 if player == X else -1
    return 0
 

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    player_turn = player(board)
    ai_action = None
    best_of_max = float("-inf")
    best_of_min = float("inf")
    
    if player_turn == X:
        best_score = float("-inf")
        for action in actions(board):
            score = min_value(result(board, action), best_of_max, best_of_min)
            if score > best_score:
                best_score = score
                ai_action = action
            best_of_max = max(best_of_max, best_score)
    else:
        best_score = float("inf")
        for action in actions(board):
            score = max_value(result(board, action), best_of_max, best_of_min)
            if score < best_score:
                best_score = score
                ai_action = action
            best_of_min = min(best_of_min, best_score)
    
    return ai_action

def max_value(board, best_of_max, best_of_min):
    if terminal(board):
        return utility(board)
    
    best_score = float("-inf")
    for action in actions(board):
        score = min_value(result(board, action), best_of_max, best_of_min)
        if score >= best_of_min:
            return score
        best_score = max(best_score, score)
        best_of_max = max(best_of_max, best_score)
    return best_score

def min_value(board, best_of_max, best_of_min):
    if terminal(board):
        return utility(board)
    
    best_score = float("inf")
    for action in actions(board):
        score = max_value(result(board, action), best_of_max, best_of_min)
        if score <= best_of_max:
            # i.e., if the score is less than what max is gonna pick, max is not going to pick it. so just keep moving on
            return score
        best_score = min(best_score, score)
        best_of_min = min(best_of_min, best_score)
    return best_score
   
