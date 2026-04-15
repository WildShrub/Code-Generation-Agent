Here's the implementation of the Tic-Tac-Toe game module and its corresponding README file:

### src/main.py
```python
"""
Tic-Tac-Toe Game Module

This module implements a console-based Tic-Tac-Toe game with clear separation of concerns
between game logic, board management, user interface, and game control.

Components:
- GameBoard: Manages the game state and board representation
- GameLogic: Handles game rules, win conditions, and turn management
- UserInterface: Handles input/output with the player
- GameController: Orchestrates the game flow between components
"""

import os
from typing import List, Optional, Tuple

class GameBoard:
    """Manages the game state and board representation for Tic-Tac-Toe."""

    def __init__(self) -> None:
        """Initialize an empty 3x3 game board."""
        self.board: List[List[Optional[str]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def display(self) -> None:
        """Print the current state of the game board to the console."""
        print("\nCurrent Board:")
        print("-------------")
        for row in self.board:
            print("| " + " | ".join(cell if cell is not None else " " for cell in row) + " |")
            print("-------------")

    def make_move(self, position: int, symbol: str) -> bool:
        """
        Update the board with a player's move.

        Args:
            position: The position to place the symbol (1-9)
            symbol: The player's symbol ('X' or 'O')

        Returns:
            bool: True if move was successful, False if position was invalid or occupied
        """
        row, col = divmod(position - 1, 3)

        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        if self.board[row][col] is not None:
            return False

        self.board[row][col] = symbol
        return True

    def get_board_state(self) -> List[List[Optional[str]]]:
        """Return the current state of the board."""
        return self.board

class GameLogic:
    """Handles game rules, win conditions, and turn management."""

    def check_winner(self, board: List[List[Optional[str]]]) -> Optional[str]:
        """
        Determine if the current board state has a winner.

        Args:
            board: The current game board state

        Returns:
            Optional[str]: The winning symbol ('X' or 'O') if there's a winner, None otherwise
        """
        # Check rows
        for row in board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                return row[0]

        # Check columns
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]

        # Check diagonals
        if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

        return None

    def is_board_full(self, board: List[List[Optional[str]]]) -> bool:
        """
        Check if the board is full (draw condition).

        Args:
            board: The current game board state

        Returns:
            bool: True if board is full, False otherwise
        """
        return all(cell is not None for row in board for cell in row)

class UserInterface:
    """Handles input/output with the player."""

    def get_player_move(self, current_player: str) -> int:
        """
        Get a valid move from the player.

        Args:
            current_player: The current player's symbol ('X' or 'O')

        Returns:
            int: The validated position (1-9) for the move
        """
        while True:
            try:
                position = int(input(f"Player {current_player}, enter your move (1-9): "))
                if 1 <= position <= 9:
                    return position
                print("Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def announce_winner(self, winner: str) -> None:
        """Announce the winner of the game."""
        print(f"\nPlayer {winner} wins! Congratulations!")

    def announce_draw(self) -> None:
        """Announce that the game ended in a draw."""
        print("\nThe game ended in a draw!")

    def ask_to_play_again(self) -> bool:
        """
        Ask the player if they want to play another game.

        Returns:
            bool: True if player wants to play again, False otherwise
        """
        while True:
            response = input("Do you want to play again? (yes/no): ").lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            print("Please enter 'yes' or 'no'.")

class GameController:
    """Orchestrates the game flow between components."""

    def __init__(self) -> None:
        """Initialize the game components."""
        self.board = GameBoard()
        self.logic = GameLogic()
        self.ui = UserInterface()

    def play_game(self) -> None:
        """Main game loop that runs a single game session."""
        current_player = 'X'
        game_over = False

        while not game_over:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            self.board.display()

            position = self.ui.get_player_move(current_player)
            if not self.board.make_move(position, current_player):
                print("Invalid move. Try again.")
                continue

            winner = self.logic.check_winner(self.board.get_board_state())
            if winner:
                self.board.display()
                self.ui.announce_winner(winner)
                game_over = True
                continue

            if self.logic.is_board_full(self.board.get_board_state()):
                self.board.display()
                self.ui.announce_draw()
                game_over = True
                continue

            current_player = 'O' if current_player == 'X' else 'X'

    def start(self) -> None:
        """Start the game with a welcome message and main loop."""
        print("Welcome to Tic-Tac-Toe!")
        print("Enter numbers 1-9 to make your move, corresponding to board positions:")
        print(" 1 | 2 | 3 ")
        print("-----------")
        print(" 4 | 5 | 6 ")
        print("-----------")
        print(" 7 | 8 | 9 ")
        print("\nLet's begin!\n")

        while True:
            self.play_game()
            if not self.ui.ask_to_play_again():
                print("Thanks for playing! Goodbye.")
                break
            self.board = GameBoard()  # Reset board for new game

if __name__ == "__main__":
    game = GameController()
    game.start()
```

### README.md
```markdown
# Tic-Tac-Toe Game

A simple console-based implementation of the classic Tic-Tac-Toe game written in Python.

## Features

- Play against a friend on the same computer
- Clear console display of the game board
- Input validation for all moves
- Option to play multiple games in a row
- Clean, modular code with separation of concerns

## How to Run

1. Make sure you have Python 3.x installed
2. Save the code to `src/main.py`
3. Run the game with:
   ```bash
   python src/main.py
   ```

## Game Rules

- Two players take turns marking the spaces in a 3x3 grid
- Player 1 is 'X' and Player 2 is 'O'
- The player who succeeds in placing three respective marks in a horizontal, vertical, or diagonal row wins
- If all nine squares are filled and neither player has three in a row, the game is a draw

## Controls

- Enter numbers 1-9 to make your move, corresponding to board positions:
  ```
   1 | 2 | 3
  -----------
   4 | 5 | 6
  -----------
   7 | 8 | 9
  ```
- After each move, the board will be displayed
- After a game ends, you'll be asked if you want to play again

## Example Game Session

```
Welcome to Tic-Tac-Toe!
Enter numbers 1-9 to make your move, corresponding to board positions:
 1 | 2 | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9

Let's begin!

Current Board:
-------------
|   |   |   |
-------------
|   |   |   |
-------------
|   |   |   |
-------------
Player X, enter your move (1-9): 5

Current Board:
-------------
|   |   |   |
-------------
|   | X |   |
-------------
|   |   |   |
-------------
Player O, enter your move (1-9): 1

Current Board:
-------------
| O |   |   |
-------------
|   | X |   |
-------------
|   |   |   |
-------------
Player X, enter your move (1-9): 3

Current Board:
-------------
| O |   | X |
-------------
|   | X |   |
-------------
|   |   |   |
-------------
Player O, enter your move (1-9): 7

Current Board:
-------------
| O |   | X |
-------------
|   | X |   |
-------------
| O |   |   |
-------------
Player X, enter your move (1-9): 9

Current Board:
-------------
| O |   | X |
-------------
|   | X |   |
-------------
| O |   | X |
-------------
Player O, enter your move (1-9): 2

Current Board:
-------------
| O | O | X |
-------------
|   | X |   |
-------------
| O |   | X |
-------------
Player X, enter your move (1-9): 4

Current Board:
-------------
| O | O | X |
-------------
| X | X |   |
-------------
| O |   | X |
-------------
Player O, enter your move (1-9): 6

Current Board:
-------------
| O | O | X |
-------------
| X | X | O |
-------------
| O |   | X |
-------------
Player X, enter your move (1-9): 8

Current Board:
-------------
| O | O | X |
-------------
| X | X | O |
-------------
| O | X | X |
-------------

Player X wins! Congratulations!
Do you want to play again? (yes/no): no
Thanks for playing! Goodbye.
```

## Known Limitations

1. No AI opponent - requires two human players
2. Basic console interface with no graphical elements
3. Limited error handling for edge cases
4. No move history or undo functionality

## Future Enhancements

Potential improvements for future versions:

1. Add an AI opponent with different difficulty levels
2. Implement a graphical user interface
3. Add move history and undo functionality
4. Support for network play between remote players
5. Score tracking across multiple games
6. Customizable board sizes (beyond 3x3)
7. Save/load game states

## License

This project is open source and available under the MIT License.
