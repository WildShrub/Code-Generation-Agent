# Tic-Tac-Toe Game

A simple console-based Tic-Tac-Toe game for two players (X and O).

## Game Description

This is a classic Tic-Tac-Toe implementation where two players take turns marking spaces in a 3x3 grid. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row wins the game.

## How to Play

1. Player X goes first, followed by Player O
2. Players take turns entering a number (1-9) corresponding to their desired position on the board
3. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
4. If all 9 squares are filled without a winner, the game ends in a draw

## Installation

No installation required. Simply run the Python script.

## Running the Game

```bash
python main.py
```

## Game Rules

- Players alternate turns
- Player X always goes first
- Valid moves are numbers 1-9 corresponding to board positions
- Invalid moves are rejected and the player must try again
- The game ends when a player gets three in a row or the board is full

## Example Gameplay

```
 1 | 2 | 3
---------
 4 | 5 | 6
---------
 7 | 8 | 9

Player X's turn (1-9): 5

 1 | 2 | 3
---------
 4 | X | 6
---------
 7 | 8 | 9

Player O's turn (1-9): 1

 X | 2 | 3
---------
 4 | X | 6
---------
 7 | 8 | 9

Player X's turn (1-9): 9

 X | 2 | 3
---------
 4 | X | 6
---------
 7 | 8 | X

Player O's turn (1-9): 3

 X | 2 | O
---------
 4 | X | 6
---------
 7 | 8 | X

Player X's turn (1-9): 7

 X | 2 | O
---------
 4 | X | 6
---------
 X | 8 | X

Player O's turn (1-9): 2

 X | O | O
---------
 4 | X | 6
---------
 X | 8 | X

Player X wins!
```

## Troubleshooting

- If you encounter input errors, ensure you're entering numbers 1-9
- The game will prompt you to re-enter if your move is invalid
- If the game crashes, check that you're using a compatible Python version (3.6+)

## Known Limitations

- No AI opponent (only two-player mode)
- No save/load functionality
- Basic console interface only
- Limited error handling for non-numeric input

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.