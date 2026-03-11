
class ConnectFour:
    def __init__(self):
        self.board = [[' '] * 7 for _ in range(6)]
        self.current_winner = None  # Tracks the winner

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('-' * 29)
        print('  '.join(map(str, range(7))))

    def available_moves(self):
        return [col for col in range(7) if self.board[0][col] == ' ']

    def empty_squares(self):
        return any(self.board[0][col] == ' ' for col in range(7))

    def make_move(self, col, letter):
        if self.board[0][col] != ' ':
            return False

        for row in reversed(self.board):
            if row[col] == ' ':
                row[col] = letter
                if self.check_winner(letter):
                    self.current_winner = letter
                return True
        return False

    def check_winner(self, letter):
        # Check horizontal
        for row in self.board:
            for col in range(4):
                if all(row[col + i] == letter for i in range(4)):
                    return True

        # Check vertical
        for col in range(7):
            for row in range(3):
                if all(self.board[row + i][col] == letter for i in range(4)):
                    return True

        # Check diagonals (/)
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == letter for i in range(4)):
                    return True

        # Check diagonals (\)
        for row in range(3):
            for col in range(3, 7):
                if all(self.board[row + i][col - i] == letter for i in range(4)):
                    return True

        return False
