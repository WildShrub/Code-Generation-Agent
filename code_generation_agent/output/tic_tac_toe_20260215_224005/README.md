# Tic-Tac-Toe Game

A simple console-based Tic-Tac-Toe game for two players (X and O) implemented in Python.

## Features

- Classic 3x3 Tic-Tac-Toe gameplay
- Turn-based play between two players
- Input validation for moves
- Automatic win/draw detection
- Clear board display after each move

## How to Run

1. Ensure you have Python 3.x installed
2. Navigate to the project directory
3. Run the game with: `python src/main.py`

## Game Rules

- Players take turns placing their symbol (X or O) on a 3x3 grid
- The first player to get 3 of their symbols in a row (horizontally, vertically, or diagonally) wins
- If all 9 squares are filled without a winner, the game ends in a draw
- Players cannot overwrite existing moves

## Controls

- Enter the row number (0-2) when prompted
- Enter the column number (0-2) when prompted
- Enter 'q' at any time to quit the game

## Example Gameplay

```
  0 1 2
0 _|_|_
  ------
1 _|_|_
  ------
2 _|_|_

Player X's turn
Enter row (0-2): 1
Enter column (0-2): 1

  0 1 2
0 _|_|_
  ------
1 _|X|_
  ------
2 _|_|_

Player O's turn
Enter row (0-2): 0
Enter column (0-2): 0

  0 1 2
0 O|_|_
  ------
1 _|X|_
  ------
2 _|_|_
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.