
from duel import Duel
from strategy_c4 import Strategy

if __name__ == "__main__":
    # Strategy.train_agent(episodes=100000,action=0)
    print("Connect Four Duel!")
    
    # # Define strategies
    player1 = Strategy.best_move_cpu # Replace with your custom strategy
    # # Replace with your custom strategy
    player2 = Strategy.manual_strategy  # Replace with your custom strategy
    # # Run duels
    duel = Duel(player1, player2)
                
    results = duel.run_duels(1)

    # Print results
    print("Results after 100 duels:")
    print(f"Player X wins: {results['X']}")
    print(f"Player O wins: {results['O']}")
    print(f"Draws: {results['Draw']}\n")
