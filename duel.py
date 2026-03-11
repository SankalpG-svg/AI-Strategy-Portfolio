import copy
from tic_tac_toe import TicTacToe

class Duel:
    def __init__(self, strategy1, strategy2):
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.results = {'X': 0, 'O': 0, 'Draw': 0}

    def play_game(self):
        game = TicTacToe()
        strategies = {'X': self.strategy1, 'O': self.strategy2}
        letter = 'X'
        while game.empty_squares():
            board = copy.deepcopy(game)
            move = strategies[letter](board, letter)
            if game.make_move(move, letter):
                if game.current_winner:
                    if letter =='X':
                       game.print_board()
                    return letter  # Current player won
                letter = 'O' if letter == 'X' else 'X'
            else:
                raise ValueError(f"Invalid move: {move} by strategy {letter}")

        return 'Draw'

    def run_duels(self, num_games=100):
        for _ in range(num_games):
            result = self.play_game()

            self.results[result] += 1
            print()

        return self.results
