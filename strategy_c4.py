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
    def get_board_id(board):
        board_str = ''.join([''.join(row) for row in board])
        return hashlib.md5(board_str.encode()).hexdigest()
    
    score = dict()

    @staticmethod
    def best_move(game, letter, max_depth   = 7 ):
        def calculate(game, letter, depth):
            board_id = Strategy.get_board_id(game.board)
            if Strategy.score.get(board_id) is not None:
                return Strategy.score[board_id]
            if game.current_winner == 'X':
                Strategy.score[board_id] = 1
                return 1
            if game.current_winner == 'O':
                Strategy.score[board_id] = -1
                return -1
            if len(game.available_moves()) == 0:
                Strategy.score[board_id] = 0
                return 0
            if max_depth == depth:
                return 0
            board_t = board_id
            if letter == 'X':
                Strategy.score[board_t] = -2
            else:
                Strategy.score[board_t] = 2
            for move in game.available_moves():
                board = copy.deepcopy(game)
                board.make_move(move, letter)
                if letter == 'X':
                    if calculate(board, 'O', depth+1) > Strategy.score[board_t]:
                        Strategy.score[board_t] = calculate(board, 'O', depth+1)
                else:
                    if calculate(board, 'X', depth+1) < Strategy.score[board_t]:
                        Strategy.score[board_t] = calculate(board, 'X', depth+1)
            return Strategy.score[board_t]
        
        calculate(game, letter, 0)
        
    @staticmethod
    def get_move(game, letter):
        depth = 5
        opponent = 'O' if letter == 'X' else 'X'
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            Strategy.best_move(board, opponent, depth   )
        Strategy.best_move(game, letter, depth)
        best_moves = []
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            Strategy.best_move(board, opponent, depth)
            if Strategy.score[tuple(Strategy.get_board_id(board.board))] == Strategy.score[tuple(Strategy.get_board_id(game.board))]:
                best_moves.append(move)
        if len(best_moves) == 0:
            return random.choice(game.available_moves())
        return random.choice(best_moves)
    
    score_cpu = dict()
    @staticmethod
    @staticmethod
    def kaggle_minimax(game, letter, depth=5):
        """
        The master entry point for the Kaggle-style Minimax algorithm with Alpha-Beta Pruning.
        Call this in your env with: Strategy.kaggle_minimax(self.game, 'O')
        """
        import numpy as np
        import math
        import random

        # 1. Translate the board to numbers for faster math (Empty=0, AI=1, Opp=2)
        mark = 1 if letter == 'X' else 2
        grid = np.zeros((6, 7), dtype=int)
        for r in range(6):
            for c in range(7):
                if game.board[r][c] == 'X':
                    grid[r][c] = 1 if mark == 1 else 2
                elif game.board[r][c] == 'O':
                    grid[r][c] = 2 if mark == 1 else 1

        valid_moves = [c for c in range(7) if grid[0][c] == 0]
        if not valid_moves:
            return random.choice(game.available_moves())

        best_score = -math.inf
        best_col = random.choice(valid_moves)
        
        # Initialize Alpha and Beta
        alpha = -math.inf
        beta = math.inf

        for col in valid_moves:
            # Simulate dropping the piece
            next_grid = Strategy._minimax_drop_piece(grid, col, mark)
            # Call the recursive minimax with alpha and beta
            score = Strategy._minimax_recursive(next_grid, depth - 1, False, mark, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_col = col
                
            # Update alpha
            alpha = max(alpha, best_score)

        return best_col

    # ==========================================
    # MINIMAX HELPER FUNCTIONS
    # ==========================================

    @staticmethod
    def _minimax_recursive(node, depth, maximizingPlayer, mark, alpha, beta):
        import numpy as np
        import math
        
        is_terminal = Strategy._is_terminal_node(node)
        valid_moves = [c for c in range(7) if node[0][c] == 0]
        
        if depth == 0 or is_terminal:
            return Strategy._get_heuristic(node, mark)
            
        if maximizingPlayer:
            value = -math.inf
            for col in valid_moves:
                child = Strategy._minimax_drop_piece(node, col, mark)
                value = max(value, Strategy._minimax_recursive(child, depth - 1, False, mark, alpha, beta))
                
                # Update Alpha
                alpha = max(alpha, value)
                
                # ALPHA-BETA PRUNING: Cut off the branch if it's useless
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            # Opponent's mark is the opposite of ours
            opp_mark = 1 if mark == 2 else 2
            for col in valid_moves:
                child = Strategy._minimax_drop_piece(node, col, opp_mark)
                value = min(value, Strategy._minimax_recursive(child, depth - 1, True, mark, alpha, beta))
                
                # Update Beta
                beta = min(beta, value)
                
                # ALPHA-BETA PRUNING: Cut off the branch if it's useless
                if beta <= alpha:
                    break
            return value

    @staticmethod
    def _minimax_drop_piece(grid, col, piece):
        """Simulates dropping a piece without altering the real game board."""
        next_grid = grid.copy()
        for row in range(5, -1, -1):
            if next_grid[row][col] == 0:
                next_grid[row][col] = piece
                break
        return next_grid

    @staticmethod
    def _is_terminal_window(window):
        return window.count(1) == 4 or window.count(2) == 4

    @staticmethod
    def _is_terminal_node(grid):
        """Checks if the game has ended (Win or Draw)."""
        # Draw
        if list(grid[0, :]).count(0) == 0:
            return True
            
        # Horizontal
        for row in range(6):
            for col in range(7 - 3):
                window = list(grid[row, col:col+4])
                if Strategy._is_terminal_window(window):
                    return True
        # Vertical
        for row in range(6 - 3):
            for col in range(7):
                window = list(grid[row:row+4, col])
                if Strategy._is_terminal_window(window):
                    return True
        # Positive Diagonal
        for row in range(6 - 3):
            for col in range(7 - 3):
                window = list(grid[range(row, row+4), range(col, col+4)])
                if Strategy._is_terminal_window(window):
                    return True
        # Negative Diagonal
        for row in range(3, 6):
            for col in range(7 - 3):
                window = list(grid[range(row, row-4, -1), range(col, col+4)])
                if Strategy._is_terminal_window(window):
                    return True
        return False

    @staticmethod
    def _check_window(window, num_discs, piece):
        """Helper to check if a window matches the exact piece count and empty spaces."""
        return window.count(piece) == num_discs and window.count(0) == 4 - num_discs

    @staticmethod
    def _count_windows(grid, num_discs, piece):
        """Scans the board and counts all valid windows for a specific piece."""
        num_windows = 0
        # horizontal
        for row in range(6):
            for col in range(7 - 3):
                window = list(grid[row, col:col+4])
                if Strategy._check_window(window, num_discs, piece):
                    num_windows += 1
        # vertical
        for row in range(6 - 3):
            for col in range(7):
                window = list(grid[row:row+4, col])
                if Strategy._check_window(window, num_discs, piece):
                    num_windows += 1
        # positive diagonal
        for row in range(6 - 3):
            for col in range(7 - 3):
                window = list(grid[range(row, row+4), range(col, col+4)])
                if Strategy._check_window(window, num_discs, piece):
                    num_windows += 1
        # negative diagonal
        for row in range(3, 6):
            for col in range(7 - 3):
                window = list(grid[range(row, row-4, -1), range(col, col+4)])
                if Strategy._check_window(window, num_discs, piece):
                    num_windows += 1
        return num_windows

    @staticmethod
    def _get_heuristic(grid, mark):
        """
        The Upgraded Brain: Scores the board using window counts.
        """
        opp_mark = 1 if mark == 2 else 2
        
        num_threes = Strategy._count_windows(grid, 3, mark)
        num_fours = Strategy._count_windows(grid, 4, mark)
        num_threes_opp = Strategy._count_windows(grid, 3, opp_mark)
        
        # +1,000,000 for a win, -100 for an opponent threat
        score = num_threes - (100 * num_threes_opp) + (1000000 * num_fours)
        return score

    @staticmethod
    def best_move_cpu(game, letter):
        def minimax(game, depth, alpha, beta, maximizing_player):
            board_id = Strategy.get_board_id(game.board)
            if board_id in Strategy.score_cpu:
                return Strategy.score_cpu[board_id]

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
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                Strategy.score_cpu[board_id] = max_eval
                return max_eval
            else:
                min_eval = float('inf')
                for move in game.available_moves():
                    board = copy.deepcopy(game)
                    board.make_move(move, 'O' if letter == 'X' else 'X')
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                Strategy.score_cpu[board_id] = min_eval
                return min_eval

        best_score_cpu = float('-inf')
        best_move = None
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            move_score_cpu = minimax(board, 5, float('-inf'), float('inf'), False)
            if move_score_cpu > best_score_cpu:
                best_score_cpu = move_score_cpu
                best_move = move
        return best_move

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

    