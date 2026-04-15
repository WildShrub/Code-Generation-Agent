src/main.py
```python
class GameBoard:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # Rows
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],  # Columns
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],  # Diagonals
            [(0, 2), (1, 1), (2, 0)]
        ]

    def display(self):
        print("\nCurrent Board:")
        print("  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} {'|'.join(cell if cell else ' ' for cell in row)}")
            if i < 2:
                print("  -----")

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and not self.board[row][col]

    def make_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.board[row][col] = symbol
            return True
        return False

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def check_winner(self):
        for combo in self.winning_combinations:
            symbols = [self.board[r][c] for r, c in combo]
            if all(s == 'X' for s in symbols) or all(s == 'O' for s in symbols):
                return symbols[0]
        return None

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self):
        while True:
            try:
                move = input(f"Player {self.symbol}, enter your move (row column): ")
                row, col = map(int, move.split())
                return row, col
            except (ValueError, IndexError):
                print("Invalid input. Please enter two numbers separated by space (e.g., '0 1').")

class GameController:
    def __init__(self):
        self.board = GameBoard()
        self.players = [Player('X'), Player('O')]
        self.current_player_index = 0

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_game_over(self):
        winner = self.board.check_winner()
        if winner:
            print(f"\nPlayer {winner} wins!")
            return True
        if self.board.is_full():
            print("\nIt's a draw!")
            return True
        return False

    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Enter moves as 'row column' (0-2 for both).")
        self.board.display()

        while True:
            current_player = self.players[self.current_player_index]
            row, col = current_player.get_move()

            if not self.board.make_move(row, col, current_player.symbol):
                print("Invalid move. Try again.")
                continue

            self.board.display()
            if self.check_game_over():
                break

            self.switch_player()

if __name__ == "__main__":
    game = GameController()
    game.play()
