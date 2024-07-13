import hashlib
import os
import random

# In-memory user database
users_db = {}

# In-memory score database
scores_db = {}

# Clear the screen
def clear_screen():
    """Clear the console screen for a fresh display."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Display the scoreboard
def display_scoreboard(player1, player2):
    """Display the current scores."""
    print(f"Scoreboard: {player1} {scores_db[player1]} - {player2} {scores_db[player2]} - Ties {scores_db['Ties']}")

# Hash a password for storing.
def hash_password(password):
    """Hash a password for storing.
    
    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# Check if the username already exists in the database.
def check_username_exists(username):
    """Check if the username already exists in the database.
    
    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    return username in users_db

# Register a new user with a username and password.
def register_user(username, password):
    """Register a new user with a username and password.
    
    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.

    Returns:
        None
    """
    if check_username_exists(username):
        print("Username already exists. Please choose a different username.")
    else:
        hashed_password = hash_password(password)
        users_db[username] = hashed_password
        print("Account created successfully!")

# Log in a user with a username and password.
def login_user(username, password):
    """Log in a user with a username and password.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    if not check_username_exists(username):
        print("Username does not exist. Please register first.")
    else:
        hashed_password = hash_password(password)
        if users_db[username] == hashed_password:
            print("Login successful!")
            return True
        else:
            print("Incorrect password. Please try again.")
    return False

# Enter the game after successful login.
def enter_game(username):
    """Enter the game after successful login.
    
    Args:
        username (str): The username of the logged-in user.

    Returns:
        None
    """
    while True:
        game_mode = input("Do you want to play single-player (s) or multiplayer (m)? ").strip().lower()
        if game_mode == 's':
            reset_scores(username, 'Computer')
            for _ in range(3):
                play_tic_tac_toe_single_player(username)
                display_scoreboard(username, 'Computer')
            while True:
                choice = input("Do you want to play another set of 3 rounds? (y/n): ").strip().lower()
                if choice == 'y':
                    reset_scores(username, 'Computer')
                    for _ in range(3):
                        play_tic_tac_toe_single_player(username)
                        display_scoreboard(username, 'Computer')
                elif choice == 'n':
                    print("Exiting the game. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.")
        elif game_mode == 'm':
            opponent = input("Enter the username of the person you want to play with: ").strip()
            if opponent == username:
                print("It's ok to play alone but dooz needs a partner!")
            elif check_username_exists(opponent):
                reset_scores(username, opponent)
                for _ in range(3):
                    play_tic_tac_toe_multiplayer(username, opponent)
                    display_scoreboard(username, opponent)
                while True:
                    choice = input("Do you want to play another set of 3 rounds? (y/n): ").strip().lower()
                    if choice == 'y':
                        reset_scores(username, opponent)
                        for _ in range(3):
                            play_tic_tac_toe_multiplayer(username, opponent)
                            display_scoreboard(username, opponent)
                    elif choice == 'n':
                        print("Exiting the game. Goodbye!")
                        return
                    else:
                        print("Invalid choice. Please enter 'y' or 'n'.")
            else:
                print("The username of your opponent does not exist.")
        else:
            print("Invalid choice. Please enter 's' or 'm'.")

# Reset the scores
def reset_scores(player1, player2):
    """Reset the scores to zero."""
    scores_db[player1] = 0
    scores_db[player2] = 0
    scores_db['Ties'] = 0

# Display the current tic-tac-toe board.
def display_board(board, player1, player2):
    """Display the current tic-tac-toe board.
    
    Args:
        board (list): The tic-tac-toe board.

    Returns:
        None
    """
    clear_screen()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("---------")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("---------")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    display_scoreboard(player1, player2)

# Check if the given player has won the game.
def check_winner(board, player):
    """Check if the given player has won the game.
    
    Args:
        board (list): The tic-tac-toe board.
        player (str): The player to check ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8)]  # Columns
                      #(0, 4, 8), (2, 4, 6)]  # Diagonals
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Check if the tic-tac-toe board is full.
def check_full(board):
    """Check if the tic-tac-toe board is full.
    
    Args:
        board (list): The tic-tac-toe board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return all(cell in ['X', 'O'] for cell in board)

# Minimax algorithm to calculate the best move for the computer.
def minimax(board, depth, is_maximizing):
    """Minimax algorithm to calculate the best move for the computer.
    
    Args:
        board (list): The tic-tac-toe board.
        depth (int): The current depth of the minimax tree.
        is_maximizing (bool): True if the algorithm is maximizing, False if minimizing.

    Returns:
        int: The score of the best move.
    """
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif check_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] not in ['X', 'O']:
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = str(i + 1)
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] not in ['X', 'O']:
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = str(i + 1)
                best_score = min(score, best_score)
        return best_score

# Find the best move for the computer using the minimax algorithm.
def best_move(board):
    """Find the best move for the computer using the minimax algorithm.
    
    Args:
        board (list): The tic-tac-toe board.

    Returns:
        int: The index of the best move.
    """
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] not in ['X', 'O']:
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = str(i + 1)
            if score > best_score:
                best_score = score
                move = i
    return move

# Play a game of tic-tac-toe against the computer.
def play_tic_tac_toe_single_player(username):
    """Play a game of tic-tac-toe against the computer.
    
    Args:
        username (str): The username of the player.

    Returns:
        None
    """
    board = [str(i + 1) for i in range(9)]
    current_player = 'X'
    while True:
        display_board(board, username, 'Computer')
        if current_player == 'X':
            move = input(f"Player {current_player}, enter your move (1-9): ").strip()
            if move.isdigit() and int(move) in range(1, 10):
                move = int(move) - 1
                if board[move] not in ['X', 'O']:
                    board[move] = current_player
                    if check_winner(board, current_player):
                        display_board(board, username, 'Computer')
                        print(f"{username} wins!")
                        scores_db[username] += 1
                        break
                    elif check_full(board):
                        display_board(board, username, 'Computer')
                        print("It's a tie!")
                        scores_db['Ties'] += 1
                        break
                    current_player = 'O'
                else:
                    print("Invalid move, cell already taken.")
            else:
                print("Invalid move, please enter a number between 1 and 9.")
        else:
            move = best_move(board)
            board[move] = current_player
            if check_winner(board, current_player):
                display_board(board, username, 'Computer')
                print("Computer wins!")
                scores_db['Computer'] += 1
                break
            elif check_full(board):
                display_board(board, username, 'Computer')
                print("It's a tie!")
                scores_db['Ties'] += 1
                break
            current_player = 'X'

# Play a game of tic-tac-toe between two players.
def play_tic_tac_toe_multiplayer(player1, player2):
    """Play a game of tic-tac-toe between two players.
    
    Args:
        player1 (str): The username of the first player.
        player2 (str): The username of the second player.

    Returns:
        None
    """
    board = [str(i + 1) for i in range(9)]
    current_player = 'X'
    player_map = {'X': player1, 'O': player2}
    while True:
        display_board(board, player1, player2)
        move = input(f"{player_map[current_player]}, enter your move (1-9): ").strip()
        if move.isdigit() and int(move) in range(1, 10):
            move = int(move) - 1
            if board[move] not in ['X', 'O']:
                board[move] = current_player
                if check_winner(board, current_player):
                    display_board(board, player1, player2)
                    print(f"{player_map[current_player]} wins!")
                    scores_db[player_map[current_player]] += 1
                    break
                elif check_full(board):
                    display_board(board, player1, player2)
                    print("It's a tie!")
                    scores_db['Ties'] += 1
                    break
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                print("Invalid move, cell already taken.")
        else:
            print("Invalid move, please enter a number between 1 and 9.")

# Main function to run the Tic-Tac-Toe game program.
def main():
    """Main function to run the Tic-Tac-Toe game program.
    
    Args:
        None

    Returns:
        None
    """
    while True:
        print("\nTic-Tac-Toe Game")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == '1':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            register_user(username, password)
        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            if login_user(username, password):
                enter_game(username)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
