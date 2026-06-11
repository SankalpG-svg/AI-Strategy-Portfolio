import hashlib
import copy
import random
from connect_four import ConnectFour
import numpy as np

class Strategy:
    @staticmethod
    def random_opstrategy(game, letter):
        return random.choice(game.available_moves())

    @staticmethod
    def first_available_strategy(game, letter):
        return game.available_moves()[0]

    @staticmethod
    def medium_strategy(game, letter):
        for move in game.available_moves():
            board = copy.deepcopy(game)
            if board.make_move(move, letter):
                if board.current_winner == letter:
                    return move  # Fixed: changed 'm' to 'move'
        return random.choice(game.available_moves())

    @staticmethod
    def harder(game, letter):  # Fixed: changed 'def harder):'
        opponent = 'O' if letter == 'X' else 'X'
        for move in game.available_moves():
            board = copy.deepcopy(game)
            if board.make_move(move, letter):
                if board.current_winner == letter:
                    return move
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            f = True
            for move_opp in board.available_moves():
                board1 = copy.deepcopy(board)
                if board1.make_move(move_opp, opponent):
                    if board1.current_winner == opponent:
                        f = False
                        break
            if f:
                return move    
        return random.choice(game.available_moves())

    @staticmethod
    def sankalp_2(game, letter):
        opponent = 'O' if letter == 'X' else 'X'
        l = len(game.available_moves())
        
        if l == 9:
            return 0
        if l == 1:
            return random.choice(game.available_moves())
            
        if l == 8:
            p = True
            for move in game.available_moves():
                if move == 4:
                    p = False
                    break
            if p == False:
                return 4 
            else:    
                return random.choice([0,2,6,8])

        if l == 7:
            for move in game.available_moves():
                if move % 4 == 0 or move % 8 == 0:
                    return move            

        for move in game.available_moves():
            board3 = copy.deepcopy(game)
            if board3.make_move(move, letter):
                if board3.current_winner == letter:
                    return move

        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            f = True
            for move_opp in board.available_moves():
                board1 = copy.deepcopy(board)
                if board1.make_move(move_opp, opponent):
                    if board1.current_winner == opponent:
                        return move
                        f = False
                        break
        if f:
            for move1 in game.available_moves():
                board = copy.deepcopy(game)
                board.make_move(move1, letter)
                for move in board.available_moves():
                    board2 = copy.deepcopy(board)
                    if board2.make_move(move, letter):
                        if board2.current_winner == letter:
                            return move1
                            break

        return random.choice(game.available_moves())

    @staticmethod
    def manual_strategy(game, letter):
        game.print_board()
        print("\n")        
        while True:
            try:
                move = int(input("Enter your move (0-6): "))
                if move in game.available_moves():
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")

    @staticmethod
    def best_move(game, letter, depth, alpha, beta, maximizing_player):
        if game.current_winner == letter:
            return 1
        elif game.current_winner == ('O' if letter == 'X' else 'X'):
            return -1
        elif not game.available_moves() or depth == 0:
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for move in game.available_moves():
                board = copy.deepcopy(game)
                board.make_move(move, letter)
                eval = Strategy.best_move(board, letter, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.available_moves():
                board = copy.deepcopy(game)
                board.make_move(move, 'O' if letter == 'X' else 'X')
                eval = Strategy.best_move(board, letter, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    @staticmethod
    def get_move(game, letter):
        # Uses depth 5 for standard minimax
        best_score = float('-inf')
        best_moves = []
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            move_score = Strategy.best_move(board, letter, 5, float('-inf'), float('inf'), False)
            if move_score > best_score:
                best_score = move_score
                best_moves = [move]
            elif move_score == best_score:
                best_moves.append(move)
        return random.choice(best_moves) if best_moves else random.choice(game.available_moves())

    @staticmethod
    def best_move_cpu(game, letter):
        # Uses depth 7 for alpha-beta
        best_score = float('-inf')
        best_moves = []
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            move_score = Strategy.best_move(board, letter, 7, float('-inf'), float('inf'), False)
            if move_score > best_score:
                best_score = move_score
                best_moves = [move]
            elif move_score == best_score:
                best_moves.append(move)
        return random.choice(best_moves) if best_moves else random.choice(game.available_moves())

    # ==========================================
    # REINFORCEMENT LEARNING SECTION (YOUR TURN)
    # ==========================================
    
    # 1. The Brain (Your Q-Table)
    q_table = {}

    @staticmethod
    def direct_reward(game, letter):
        if game.current_winner == letter:
            return 1  # Win
        elif game.current_winner == ('O' if letter == 'X' else 'X'):
            return -1  # Loss
        elif not game.available_moves():
            return 0  # Draw
        else:
            return 0  # Ongoing game
    
    @staticmethod
    def get_q_values(game,Letter):
        id = Strategy.get_board_id(game.board)
        # If not in table, initialize it with 7 zeros permanently
        if id not in Strategy.q_table:
            Strategy.q_table[id] = [0.0] * 7
        return Strategy.q_table[id]
    @staticmethod
    def update_q_table(game, letter, move, reward, gamma=0.95, peek_board=None):
        id=Strategy.get_board_id(game.board)
        current_q_values = Strategy.get_q_values(game, letter)
        future_rewards = Strategy.get_q_values(peek_board, letter)
        Strategy.q_table[id][move] = 0.05*current_q_values[move]+ 0.95*(reward + gamma * max(future_rewards))

    @staticmethod
    def RL(game, letter, epsilon=0.1):
        import random
        
        # 1. Exploration: 10% of the time, pick a completely random move
        if random.random() < epsilon:
            return random.choice(game.available_moves())
            
        # 2. Exploitation: Look at the 7 values for the current board
        q_values = Strategy.get_q_values(game, letter)
        
        mx = -float('inf')
        best_move = -1
        
        # 3. Find the valid column with the highest score
        for move in game.available_moves():
            if q_values[move] > mx:
                mx = q_values[move]
                best_move = move
                
        return best_move
    @staticmethod
    def train_agent(episodes=10000,action=None):    
        """
        Trains the RL agent by making it play thousands of games 
        against a random opponent.
        """
        import random
        
        epsilon = 1.0        # Start by exploring 100% of the time
        epsilon_decay = 0.999 # Multiply epsilon by this after every game
        min_epsilon = 0.05    # Never drop exploration below 5%
        
        print(f"Starting training for {episodes} episodes...")
        
        for episode in range(episodes):
            game = ConnectFour() 
            turn = 'X'# Start a fresh board
            if action == 1:
                turn = 'O'           # Let the RL agent go first
                      # Let the RL agent go first
            
            while game.empty_squares() and game.current_winner is None:
                if turn == 'O':
                    # --- THE AGENT's TURN ---
                    
                    # 1. Ask the RL brain to pick a move
                    move = Strategy.RL(game, 'O', epsilon)
                    
                    # 2. Peek into the future to see what the direct reward is
                    peek_board = copy.deepcopy(game)
                    peek_board.make_move(move, 'O')
                    reward = Strategy.direct_reward(peek_board, 'O')
                    
                    # 3. LEARN! Update the Q-Table before we actually move
                    Strategy.update_q_table(game, 'O', move, reward, peek_board=peek_board)
                    
                    # 4. Actually drop the piece on the real board
                    game.make_move(move, 'O')
                    
                else:
                    # --- THE OPPONENT'S TURN ---
                    # For now, it trains against a bot that plays completely randomly
                    move = Strategy.random_opstrategy(game, 'X')
                    game.make_move(move, 'X')
                
                # Swap turns!
                turn = 'O' if turn == 'X' else 'X'
                
            # --- END OF GAME ---
            # Shrink epsilon slightly so it gets smarter over time
            epsilon = max(min_epsilon, epsilon * epsilon_decay)
            
            # Print an update every 1000 games so you know it hasn't frozen
            if episode % 1000 == 0:
                print(f"Episode {episode} completed. Current Epsilon: {epsilon:.3f}")
                
        print("Training Complete! The Q-Table is now populated.")
                   
    import numpy as np
    from stable_baselines3 import PPO

    # Load the brain! (We put this outside the method so it only loads once)
    try:
        cnn_model = PPO.load("custom_connect4_cnn")
    except Exception as e:
        print(f"🚨 CRITICAL LOADING ERROR: {e}")
        cnn_model = None

    @staticmethod
    def cnn_strategy(game, letter):
        if Strategy.cnn_model is None:
            return random.choice(game.available_moves())

        # FIX 1: Must match the float32 type from the gym environment
        obs = np.zeros((1, 6, 7), dtype=np.float32)
        
        # Identify who is the opponent
        opponent_letter = 'O' if letter == 'X' else 'X'

        for r in range(6):
            for c in range(7):
                if game.board[r][c] == letter:
                    obs[0][r][c] = 1.0  # AI's pieces are 1.0
                elif game.board[r][c] == opponent_letter:
                    obs[0][r][c] = -1.0 # FIX 2: Enemy pieces MUST be -1.0 to match training!

        # Predict the action
        action, _states = Strategy.cnn_model.predict(obs, deterministic=True)
        best_move = int(action)
        
        if best_move not in game.available_moves():
            return random.choice(game.available_moves())
            
        return best_move       

    @staticmethod
    def column_stacker(game, token):
        # If the bot hasn't chosen a column yet, or if its chosen column is full
        if not hasattr(Strategy, '_target_col') or Strategy._target_col not in game.available_moves():
            if game.available_moves():
                Strategy._target_col = random.choice(game.available_moves())
            else:
                return random.choice(game.available_moves())
        
        return Strategy._target_col       

    