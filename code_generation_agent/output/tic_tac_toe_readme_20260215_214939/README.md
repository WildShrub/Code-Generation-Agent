# Tic-Tac-Toe Game

A simple console-based Tic-Tac-Toe game for two players (X and O) implemented in Python.

## Features

- Classic 3x3 Tic-Tac-Toe gameplay
- Turn-based system with player validation
- Win detection for all possible winning combinations
- Draw detection when the board is full
- Random player start to ensure fairness
- No external dependencies (uses only Python standard library)

## How to Run

1. Ensure you have Python 3.x installed
2. Save the code as `main.py`
3. Run the game with: `python main.py`

## Game Rules

- Two players take turns marking spaces in a 3x3 grid
- Player X goes first (unless random selection chooses O)
- Players alternate turns until one wins or the board is full
- The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
- If all spaces are filled with no winner, the game ends in a draw

## Controls

- Enter a number (1-9) to make your move, corresponding to board positions:
  ```
  1 | 2 | 3
  ---------
  4 | 5 | 6
  ---------
  7 | 8 | 9
  ```
- Enter 'q' at any time to quit the game

## Example Gameplay

```
Welcome to Tic-Tac-Toe!
Player X will go first.

Current Board:
 1 | 2 | 3
 ---------
 4 | 5 | 6
 ---------
 7 | 8 | 9

Player X's turn (1-9 or q to quit): 5

Current Board:
 1 | 2 | 3
 ---------
 4 | X | 6
 ---------
 7 | 8 | 9

Player O's turn (1-9 or q to quit): 1

Current Board:
 O | 2 | 3
 ---------
 4 | X | 6
 ---------
 7 | 8 | 9

... (game continues until win or draw) ...
```

## License

This project is open source and available under the MIT License.