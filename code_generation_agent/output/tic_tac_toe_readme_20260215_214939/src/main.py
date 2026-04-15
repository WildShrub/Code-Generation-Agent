import random
import sys

class Board:
    """Represents the Tic-Tac-Toe game board."""

    def __init__(self):
        self.board = self.initialize_board()

    def initialize_board(self):
        """Initialize a 3x3 empty board."""
        return [[' ' for _ in range(3)] for _ in range(3)]

    def print_board(self):
        """Display the current board state."""
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def is_valid_move(self, row, col):
        """Check if a move is valid (within bounds and empty)."""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '

    def make_move(self, row, col, player):
        """Place a player's symbol on the board."""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def check_winner(self):
        """Check if there's a winner."""
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_draw(self):
        """Check if the game is a draw."""
        return all(cell != ' ' for row in self.board for cell in row)

class Player:
    """Represents a Tic-Tac-Toe player."""

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self):
        """Get a valid move from the player."""
        while True:
            try:
                move = input(f"Player {self.symbol}, enter your move (row[0-2] col[0-2]): ")
                row, col = map(int, move.split())
                if 0 <= row < 3 and 0 <= col < 3:
                    return row, col
                print("Invalid input. Please enter row and column between 0 and 2.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")

class Game:
    """Manages the Tic-Tac-Toe game flow."""

    def __init__(self):
        self.board = Board()
        self.players = [Player('X'), Player('O')]
        self.current_player = random.choice(self.players)

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def play(self):
        """Run the main game loop."""
        print("Welcome to Tic-Tac-Toe!")
        print("Enter moves as 'row col' (e.g., '0 1' for top-middle).")
        print(f"Player {self.current_player.symbol} goes first.\n")

        while True:
            self.board.print_board()
            row, col = self.current_player.get_move()

            if not self.board.make_move(row, col, self.current_player.symbol):
                print("Invalid move. Try again.")
                continue

            winner = self.board.check_winner()
            if winner:
                self.board.print_board()
                print(f"Player {winner} wins!")
                break

            if self.board.is_draw():
                self.board.print_board()
                print("It's a draw!")
                break

            self.switch_player()

def main():
    """Entry point for the Tic-Tac-Toe game."""
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
