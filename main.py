
from strategy import Strategy
from duel import Duel
from strategy import Strategy

if __name__ == "__main__":
    print("Tic Tac Toe Duel!")

    # Define strategies
    player1 = Strategy.sankalp_2# Replace with your custom strategy
    # Replace with your custom strategy
    player2 = Strategy.manual_strategy# Replace with your custom strategy
    # Run duels
    duel = Duel(player2, player1)
    results = duel.run_duels(1)

    # Print results
    print("Results after 100 duels:")
    print(f"Player X wins: {results['X']}")
    print(f"Player O wins: {results['O']}")
    print(f"Draws: {results['Draw']}\n")
