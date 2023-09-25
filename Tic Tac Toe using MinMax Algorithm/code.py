import random

# Represents the game board
board = [[' ' for i in range(3)] for i in range(3)]

# Player and opponent symbols
player = 'X'
opponent = 'O'

# Function to print the board
def print_board():
    for row in board:
        print('|'.join(row))
        print('-' * 5)

# Function to check if the board is full
def is_board_full():
    for row in board:
        if ' ' in row:
            return False
    return True

# Function to check if a player has won
def is_winner(player):
    # Check rows
    for row in board:
        if row.count(player) == 3:
            return True

    # Check columns
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 3:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


# Utility function to evaluate the game state
def evaluate():
    if is_winner(opponent):
        return 1  # opponent wins
    elif is_winner(player):
        return -1  # Player wins
    else:
        return 0  # Draw


# Alpha-Beta Search function
def alpha_beta_search():
    best_score = float('-inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = opponent
                move_score = min_value(float('-inf'), float('inf'))
                board[row][col] = ' '

                if move_score > best_score:
                    best_score = move_score
                    best_move = (row, col)

    return best_move


# Max-Value function for Alpha-Beta Pruning
def max_value(alpha, beta):
    score = evaluate()

    if score != 0:
        return score

    max_eval = float('-inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = opponent
                eval_score = min_value(alpha, beta)
                board[row][col] = ' '

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if alpha >= beta:
                    return max_eval

    return max_eval


# Min-Value function for Alpha-Beta Pruning
def min_value(alpha, beta):
    score = evaluate()

    if score != 0:
        return score

    min_eval = float('inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = player
                eval_score = max_value(alpha, beta)
                board[row][col] = ' '

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    return min_eval

    return min_eval


# Function to make opponent move
def opponent_move():
    best_move = alpha_beta_search()

    if best_move:
        board[best_move[0]][best_move[1]] = opponent
        


# Function to handle player move
def player_move():
    while True:
        try:
            print("Enter Your Move....\n")
            row = int(input('Enter the row (1-3): '))-1
            col = int(input('Enter the column (1-3): '))-1
            if board[row][col] == ' ':
                board[row][col] = player
                break
            else:
                print('Invalid move. Try again.')
        except (ValueError, IndexError):
            print('Invalid input. Try again.')


def play_game():
    print('Tic Tac Toe - You are X and opponent is O\n')
    print_board()

    # Randomly determine the starting player
    starting_player = random.choice(['player', 'opponent'])

    while not is_board_full():
        if starting_player == 'player':
            player_move()
            print_board()

            if is_winner(player):
                print('Congratulations! You won!')
                return

            if is_board_full():
                break

            print('opponent is making a move...')
            opponent_move()
            print_board()

            if is_winner(opponent):
                print('You Lose! Better Luck Next Time!')
                return

        else:
            print('opponent is making a move...')
            opponent_move()
            print_board()

            if is_winner(opponent):
                print('You Lose! Better Luck Next Time!')
                return

            if is_board_full():
                break

            player_move()
            print_board()

            if is_winner(player):
                print('Congratulations! You won!')
                return

    print('It\'s a draw!')

play_game()
