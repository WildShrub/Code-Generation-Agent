Here's the implementation of the Tic-Tac-Toe game module and its corresponding README.md file:

### src/main.py
```python
"""
Tic-Tac-Toe Game Module

This module implements a console-based Tic-Tac-Toe game with two players (X and O).
The game follows standard Tic-Tac-Toe rules and provides a clean, modular design.

Classes:
    Board: Manages the game board state and validation
    Player: Represents a player with a symbol (X or O)
    Display: Handles console output and formatting
    InputHandler: Manages user input and validation
    Game: Main controller for the game flow
"""

from typing import List, Tuple, Optional, Union

class Board:
    """Manages the game board state and validation."""

    def __init__(self) -> None:
        """Initialize an empty 3x3 game board."""
        self.grid: List[List[Optional[str]]] = [[None for _ in range(3)] for _ in range(3)]

    def make_move(self, player: 'Player', row: int, col: int) -> bool:
        """
        Place a player's symbol on the board at the specified position.

        Args:
            player: The player making the move
            row: Row index (0-2)
            col: Column index (0-2)

        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False

        self.grid[row][col] = player.symbol
        return True

    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid (within bounds and cell is empty).

        Args:
            row: Row index to check
            col: Column index to check

        Returns:
            bool: True if move is valid, False otherwise
        """
        return (0 <= row < 3 and
                0 <= col < 3 and
                self.grid[row][col] is None)

    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner by examining rows, columns, and diagonals.

        Returns:
            Optional[str]: The winning player's symbol (X or O) or None if no winner
        """
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] is not None:
                return row[0]

        # Check columns
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] is not None:
                return self.grid[0][col]

        # Check diagonals
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] is not None or
            self.grid[0][2] == self.grid[1][1] == self.grid[2][0] is not None):
            return self.grid[1][1]

        return None

    def is_full(self) -> bool:
        """Check if the board is completely filled (draw condition)."""
        return all(cell is not None for row in self.grid for cell in row)

    def get_cell(self, row: int, col: int) -> Optional[str]:
        """
        Get the content of a specific cell.

        Args:
            row: Row index
            col: Column index

        Returns:
            Optional[str]: The cell's content or None if empty
        """
        return self.grid[row][col]

class Player:
    """Represents a player with a symbol (X or O)."""

    def __init__(self, symbol: str) -> None:
        """
        Initialize a player with a symbol.

        Args:
            symbol: Player's symbol ('X' or 'O')
        """
        if symbol not in ('X', 'O'):
            raise ValueError("Symbol must be either 'X' or 'O'")
        self.symbol = symbol

    def __str__(self) -> str:
        """Return the player's symbol as string representation."""
        return self.symbol

class Display:
    """Handles console output and formatting for the game."""

    @staticmethod
    def show_board(board: Board) -> None:
        """Display the current state of the board."""
        print("\nCurrent Board:")
        print("-------------")
        for row in board.grid:
            print("| " + " | ".join(cell if cell is not None else " " for cell in row) + " |")
            print("-------------")

    @staticmethod
    def show_message(message: str) -> None:
        """Display a message to the user."""
        print(f"\n{message}")

    @staticmethod
    def show_winner(winner: str) -> None:
        """Display the winner of the game."""
        print(f"\nPlayer {winner} wins! 🎉")

    @staticmethod
    def show_draw() -> None:
        """Display a draw message."""
        print("\nThe game ended in a draw! 🤝")

class InputHandler:
    """Manages user input and validation."""

    @staticmethod
    def get_move() -> Tuple[int, int]:
        """
        Get and validate player move input.

        Returns:
            Tuple[int, int]: Valid row and column indices
        """
        while True:
            try:
                move = input("Enter your move (row column, 0-2): ").strip()
                row, col = map(int, move.split())
                if 0 <= row <= 2 and 0 <= col <= 2:
                    return row, col
                print("Please enter numbers between 0 and 2.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by space.")

class Game:
    """Main controller for the Tic-Tac-Toe game flow."""

    def __init__(self) -> None:
        """Initialize the game with players and board."""
        self.board = Board()
        self.players = [Player('X'), Player('O')]
        self.current_player_index = 0
        self.display = Display()
        self.input_handler = InputHandler()

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player_index = 1 - self.current_player_index

    def play(self) -> None:
        """Run the main game loop."""
        self.display.show_message("Welcome to Tic-Tac-Toe!")
        self.display.show_message("Player X goes first. Enter moves as 'row column' (0-2).")

        while True:
            current_player = self.players[self.current_player_index]
            self.display.show_board(self.board)
            self.display.show_message(f"Player {current_player}'s turn")

            row, col = self.input_handler.get_move()

            if not self.board.make_move(current_player, row, col):
                self.display.show_message("Invalid move. Try again.")
                continue

            winner = self.board.check_winner()
            if winner:
                self.display.show_board(self.board)
                self.display.show_winner(winner)
                break

            if self.board.is_full():
                self.display.show_board(self.board)
                self.display.show_draw()
                break

            self.switch_player()

if __name__ == "__main__":
    game = Game()
    game.play()
```

### README.md
```markdown
# Tic-Tac-Toe Game

A simple console-based implementation of the classic Tic-Tac-Toe game for two players.

## Features

- Two-player game (X and O)
- Input validation
- Win detection (rows, columns, diagonals)
- Draw detection
- Clear console display
- Modular design with separation of concerns

## How to Run

1. Save the code to `src/main.py`
2. Run the game with Python 3:
   ```bash
   python src/main.py
   ```

## Game Rules

1. The game is played on a 3x3 grid
2. Player X goes first, followed by Player O
3. Players take turns marking an available cell
4. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
5. If all cells are filled and no player has 3 in a row, the game is a draw

## Controls

- Enter moves as two numbers separated by space (e.g., "1 2" for row 1, column 2)
- Valid row and column values are 0, 1, or 2
- The game will prompt you for valid input if you enter invalid values

## Example Gameplay

```
Welcome to Tic-Tac-Toe!
Player X goes first. Enter moves as 'row column' (0-2).

Current Board:
-------------
|   |   |   |
-------------
|   |   |   |
-------------
|   |   |   |
-------------

Player X's turn
Enter your move (row column, 0-2): 1 1

Current Board:
-------------
|   |   |   |
-------------
|   | X |   |
-------------
|   |   |   |
-------------

Player O's turn
Enter your move (row column, 0-2): 0 0

Current Board:
-------------
| O |   |   |
-------------
|   | X |   |
-------------
|   |   |   |
-------------

...
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
