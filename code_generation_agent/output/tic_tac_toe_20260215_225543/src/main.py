"""
Tic-Tac-Toe Game Implementation

A console-based Tic-Tac-Toe game for two players (X and O) with proper state management,
input validation, and error handling.
"""

from enum import Enum, auto
from typing import List, Tuple, Optional, Dict

class GameState(Enum):
    """Enumeration representing the possible states of the game."""
    IN_PROGRESS = auto()
    X_WIN = auto()
    O_WIN = auto()
    DRAW = auto()

class GameBoard:
    """Manages the 3x3 game board state and related operations."""

    def __init__(self) -> None:
        """Initialize an empty 3x3 game board."""
        self._board: List[List[str]] = [['' for _ in range(3)] for _ in range(3)]
        self._position_map: Dict[int, Tuple[int, int]] = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }
        self._win_conditions: List[Tuple[Tuple[int, int], ...]] = [
            # Rows
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            # Columns
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            # Diagonals
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0))
        ]

    def display(self) -> None:
        """Print the current state of the game board to the console."""
        print("\nCurrent Board:")
        print("-------------")
        for row in self._board:
            print("| " + " | ".join(cell if cell else " " for cell in row) + " |")
            print("-------------")

    def update(self, position: int, symbol: str) -> bool:
        """
        Update the board at the specified position with the given symbol.

        Args:
            position: The position (1-9) to update
            symbol: The symbol (X or O) to place

        Returns:
            bool: True if the update was successful, False otherwise
        """
        if not self.is_valid_move(position):
            return False

        row, col = self._position_map[position]
        self._board[row][col] = symbol
        return True

    def is_valid_move(self, position: int) -> bool:
        """
        Check if a move to the specified position is valid.

        Args:
            position: The position (1-9) to check

        Returns:
            bool: True if the move is valid, False otherwise
        """
        if position not in self._position_map:
            return False

        row, col = self._position_map[position]
        return self._board[row][col] == ''

    def is_full(self) -> bool:
        """Check if the board is completely filled."""
        return all(cell != '' for row in self._board for cell in row)

    def check_winner(self) -> Optional[str]:
        """
        Check if there is a winner on the board.

        Returns:
            Optional[str]: The winning symbol (X or O) if there is a winner,
                          None otherwise
        """
        for condition in self._win_conditions:
            symbols = [self._board[r][c] for r, c in condition]
            if all(s == 'X' for s in symbols):
                return 'X'
            if all(s == 'O' for s in symbols):
                return 'O'
        return None

class InputValidator:
    """Handles validation of user input for the game."""

    @staticmethod
    def validate_position(position: str) -> bool:
        """
        Validate that the input is a valid position (1-9).

        Args:
            position: The input string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            pos = int(position)
            return 1 <= pos <= 9
        except ValueError:
            return False

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        Validate that the symbol is either X or O.

        Args:
            symbol: The symbol to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return symbol.upper() in ('X', 'O')

class GameController:
    """Orchestrates the game flow and state management."""

    def __init__(self) -> None:
        """Initialize the game controller with a new board and state."""
        self._board = GameBoard()
        self._current_player = 'X'
        self._game_state = GameState.IN_PROGRESS
        self._validator = InputValidator()

    def get_current_player(self) -> str:
        """Get the symbol of the current player."""
        return self._current_player

    def play_turn(self, position: str) -> bool:
        """
        Execute a player's turn with the given position.

        Args:
            position: The position (1-9) to play

        Returns:
            bool: True if the turn was successful, False otherwise
        """
        if not self._validator.validate_position(position):
            return False

        pos = int(position)
        if not self._board.is_valid_move(pos):
            return False

        if not self._board.update(pos, self._current_player):
            return False

        winner = self._board.check_winner()
        if winner:
            self._game_state = GameState.X_WIN if winner == 'X' else GameState.O_WIN
            return True

        if self._board.is_full():
            self._game_state = GameState.DRAW
            return True

        self._current_player = 'O' if self._current_player == 'X' else 'X'
        return True

    def check_game_over(self) -> bool:
        """Check if the game is over (win or draw)."""
        return self._game_state != GameState.IN_PROGRESS

    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self._game_state

    def declare_winner(self) -> str:
        """
        Get the result message based on the current game state.

        Returns:
            str: The result message
        """
        if self._game_state == GameState.X_WIN:
            return "Player X wins!"
        elif self._game_state == GameState.O_WIN:
            return "Player O wins!"
        elif self._game_state == GameState.DRAW:
            return "The game is a draw!"
        return "Game in progress..."

class Display:
    """Handles the display of game information to the console."""

    @staticmethod
    def show_board(board: GameBoard) -> None:
        """Display the current game board."""
        board.display()

    @staticmethod
    def show_message(message: str) -> None:
        """Display a message to the user."""
        print(f"\n{message}")

    @staticmethod
    def show_prompt(player: str) -> None:
        """Show the prompt for the current player."""
        print(f"\nPlayer {player}, enter your move (1-9): ", end='')

class InputHandler:
    """Handles user input for the game."""

    def get_player_move(self) -> str:
        """
        Get and validate a move from the player.

        Returns:
            str: The validated move position
        """
        while True:
            try:
                move = input().strip()
                if not move:
                    print("Error: Input cannot be empty. Please try again.")
                    continue

                if not InputValidator.validate_position(move):
                    print("Error: Invalid position. Please enter a number between 1 and 9.")
                    continue

                return move
            except EOFError:
                print("\nError: Unexpected end of input. Please try again.")
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                exit(0)

def main() -> None:
    """Main game loop for the Tic-Tac-Toe game."""
    controller = GameController()
    display = Display()
    handler = InputHandler()

    print("Welcome to Tic-Tac-Toe!")
    print("Enter a number (1-9) to make your move:")
    display.show_board(controller._board)

    while not controller.check_game_over():
        current_player = controller.get_current_player()
        display.show_prompt(current_player)

        move = handler.get_player_move()
        if not controller.play_turn(move):
            print("Invalid move. Please try again.")
            continue

        display.show_board(controller._board)

    result = controller.declare_winner()
    display.show_message(result)

if __name__ == "__main__":
    main()
