import sys

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def display_board(self):
        print("\n")
        print("  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} {row[0]}|{row[1]}|{row[2]}")
            if i < 2:
                print("  -----")
        print("\n")

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play(self):
        while True:
            self.display_board()
            print(f"Player {self.current_player}'s turn")

            try:
                row, col = map(int, input("Enter row and column (0-2): ").split())
                if not self.make_move(row, col):
                    print("Invalid move. Try again.")
                    continue
            except (ValueError, IndexError):
                print("Invalid input. Please enter two numbers between 0 and 2.")
                continue

            winner = self.check_winner()
            if winner:
                self.display_board()
                print(f"Player {winner} wins!")
                break

            if self.is_board_full():
                self.display_board()
                print("It's a draw!")
                break

            self.switch_player()

        if input("Play again? (y/n): ").lower() == 'y':
            self.__init__()
            self.play()
        else:
            print("Thanks for playing!")

def main():
    game = TicTacToe()
    game.play()

if __name__ == "__main__":
    main()
