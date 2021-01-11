import numpy as np

#Utils

def make_move(board,move,player_number):
    """
    This function will execute the move (integer column number) on the given board, 
    where the acting player is given by player_number
    """
    row = 0
    while row < 6 and board[row,move] == 0:
        row += 1
    board[row-1,move] = player_number

def get_valid_moves(board):
    """
    This function will return a list with all the valid moves (column numbers)
    for the input board
    """
    valid_moves = []
    for c in range(7):
        if 0 in board[:,c]:
            valid_moves.append(c)
    return valid_moves

def is_winning_state(board, player_num):
    """
    This function will tell if the player_num player is
    winning in the board that is input
    """
    player_win_str = '{0}{0}{0}{0}'.format(player_num)
    to_str = lambda a: ''.join(a.astype(str))

    def check_horizontal(b):
        for row in b:
            if player_win_str in to_str(row):
                return True
        return False

    def check_verticle(b):
        return check_horizontal(b.T)

    def check_diagonal(b):
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b
            
            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player_win_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player_win_str in diag:
                        return True

        return False

    return (check_horizontal(board) or
            check_verticle(board) or
            check_diagonal(board))

#The players!

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number  #This is the id of the player this AI is in the game
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.other_player_number = 1 if player_number == 2 else 2  #This is the id of the other player
        self.num = 0

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        score = float('-inf')

        #value = self.max_value(board, float('-inf'), float('inf'), 5)
        valid_moves = get_valid_moves(board)
        max_move = None
        for move in valid_moves:
            temp = board.copy()
            make_move(temp, move, self.player_number)
            value = self.min_value(temp, float('-inf'), float('inf'), 4)
            if value > score:
                score = value
                max_move = move
        return max_move
        # raise NotImplementedError('Whoops I don\'t know what to do')

    def is_terminal_node(self, board):
        return is_winning_state(board, self.player_number) or is_winning_state(board, self.other_player_number) or len(get_valid_moves(board)) == 0

    def max_value(self, board, a, b, depth):
        valid_moves = get_valid_moves(board)
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluation_function(board)

        alpha = a
        for move in valid_moves:
            value = float("-inf")
            if alpha < b:
                temp = board.copy()
                make_move(temp, move, self.player_number)
                value = self.min_value(temp, alpha, b, depth - 1)
            if value > alpha:
                alpha = value
        return alpha

    def min_value(self, board, a, b, depth):
        valid_moves = get_valid_moves(board)
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluation_function(board)

        beta = b
        for move in valid_moves:
            value = float('inf')
            if a < beta:
                temp = board.copy()
                make_move(temp, move, self.other_player_number)
                value = self.max_value(temp, a, beta, depth - 1)
            if value < beta:
                beta = value
        return beta

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        score = float('-inf')

        # value = self.max_value(board, float('-inf'), float('inf'), 5)
        valid_moves = get_valid_moves(board)
        max_move = None
        for move in valid_moves:
            temp = board.copy()
            make_move(temp, move, self.player_number)
            value = self.min_value_2(temp, float('-inf'), float('inf'), 4)
            if value > score:
                score = value
                max_move = move
        return max_move

        #raise NotImplementedError('Whoops I don\'t know what to do')

    def min_value_2(self, board, a, b, depth):
        valid_moves = get_valid_moves(board)
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluation_function(board)

        beta = b
        for move in valid_moves:
            value = 0
            if a < beta:
                temp = board.copy()
                make_move(temp, move, self.other_player_number)
                value = value + (1 / len(valid_moves)) * self.max_value_2(temp, a, beta, depth - 1)
            if value < beta:
                beta = value
        return beta

    def max_value_2(self, board, a, b, depth):
        valid_moves = get_valid_moves(board)
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluation_function(board)

        alpha = a
        for move in valid_moves:
            value = 0
            if alpha < b:
                temp = board.copy()
                make_move(temp, move, self.player_number)
                value = value + (1 / len(valid_moves)) * self.min_value_2(temp, alpha, b, depth - 1)
            if value > alpha:
                alpha = value
        return alpha

    def count(self, board, length, player):
        count = 0
        for r in range(board.shape[0]):
            for c in range(board.shape[1]):
                if board[r][c] == player:
                    count = count + self.count_vertical(board, r, c, length) + self.count_horizontal(board, r, c, length) + (self.count_diagonal1(board, r, c, length) + self.count_diagonal2(board, r, c, length))
        return count

    def count_diagonal1(self, board, row, column, length):
        count = 0
        c_index = column
        for r in range(row, -1, -1):
            if c_index > 6:
                break
            elif board[row][c_index] == board[row][column]:
                count = count + 1
            else:
                break
            c_index = c_index + 1
        if count >= length:
            return 1
        else:
            return 0

    def count_diagonal2(self, board, row, column, length):
        count = 0
        c_index = column
        for r in range(row, 6):
            if c_index > 6:
                break
            elif board[r][c_index] == board[row][column]:
                count = count + 1
            else:
                break
            c_index = c_index + 1
        if count >= length:
            return 1
        else:
            return 0

    def count_vertical(self, board, row, column, length):
        count = 0
        for r in range(row, board.shape[0]):
            if board[r][column] == board[row][column]:
                count = count + 1
            else:
                break
        if length <= count:
            return 1
        else:
            return 0

    def count_horizontal(self, board, row, column, length):
        count = 0
        for c in range(column, board.shape[1]):
            if board[row][c] == board[row][column]:
                count = count + 1
            else:
                break
        if length <= count:
            return 1
        else:
            return 0

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        value = self.count(board, 4, self.player_number) * 9000 + self.count(board, 3, self.player_number) * 400 + self.count(board, 2, self.player_number) * 50
        other = self.count(board, 4, self.other_player_number) * 9000 + self.count(board, 3, self.other_player_number) * 400 + self.count(board, 2, self.other_player_number) * 50
        return value - other


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

