import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from connect_four import ConnectFour 
from strategy_c4 import Strategy

class ConnectFourGym(gym.Env):
    def __init__(self):
        super(ConnectFourGym, self).__init__()
        self.game = ConnectFour()
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            low=-1.0, 
            high=1.0, 
            shape=(1, 6, 7), 
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = ConnectFour()
        
        from strategy_c4 import Strategy
        if hasattr(Strategy, '_target_col'):
            delattr(Strategy, '_target_col')

        # === NEW: MID-GAME CLUTTER ===
        # 50% of the time, fast-forward the game by playing 2 to 6 safe random moves
        if random.random() < 0.50:
            for _ in range(random.randint(2, 6)):
                # Pick random columns, alternating turns safely
                if self.game.available_moves():
                    col = random.choice(self.game.available_moves())
                    self.game.make_move(col, 'X')
                    if self.game.available_moves():
                        col2 = random.choice(self.game.available_moves())
                        self.game.make_move(col2, 'O')

        # === MULTI-THREAT BOOT CAMP 2.0 ===
        if random.random() < 0.30:
            trap_type = random.choice(["vertical", "horizontal"])
            
            if trap_type == "vertical" and self.game.available_moves():
                threat_col = random.choice(self.game.available_moves())
                # Only drop pieces if the column isn't full from the clutter
                if self.game.board[0][threat_col] == ' ':
                    self.game.make_move(threat_col, 'O')
                    self.game.make_move(threat_col, 'O')
                    self.game.make_move(threat_col, 'O')
                    Strategy._target_col = threat_col 
                
            elif trap_type == "horizontal":
                start_col = random.randint(1, 3)
                # Quick safety check to ensure bottom row is empty here
                if self.game.board[5][start_col] == ' ':
                    self.game.make_move(start_col, 'O')
                    self.game.make_move(start_col + 1, 'O')
                    self.game.make_move(start_col + 2, 'O')
                    Strategy._target_col = random.choice([start_col - 1, start_col + 3])
                
            return self._get_obs(), {}
            
        # Normal game start
        if random.choice([True, False]) and self.game.available_moves():
            opp_move = random.choice(self.game.available_moves())
            self.game.make_move(opp_move, 'O')
            
        return self._get_obs(), {}

    def _get_obs(self):
        # Convert board tokens into numbers: Empty=0, AI (X)=1, Opponent (O)=-1
        board_matrix = np.zeros((6, 7), dtype=np.float32)
        for r in range(6):
            for c in range(7):
                piece = self.game.board[r][c]  
                if piece == 'X':
                    board_matrix[r][c] = 1.0
                elif piece == 'O':
                    board_matrix[r][c] = -1.0
                    
        # Add the channel dimension so the shape becomes (1, 6, 7)
        return np.expand_dims(board_matrix, axis=0)

    def step(self, action):
        if action not in self.game.available_moves():
            return self._get_obs(), -10.0, True, False, {}

        # 1. The AI (X) plays its turn
        self.game.make_move(action, 'X')

        if self.game.current_winner == 'X':
            return self._get_obs(), 1.0, True, False, {}  
        elif not self.game.available_moves():
            return self._get_obs(), 0.0, True, False, {}

        # === THE RUTHLESS PUNISHER CURRICULUM ===
        roll = random.randint(1, 100)
        
        if roll <= 50:
            # 50% Minimax: The elite endgame punisher. If AI ignores defense, it dies.
            opp_move = Strategy.best_move_cpu(self.game, 'O')
            
        elif roll <= 80:
            # 30% Sankalp_2: A highly aggressive intermediate bot.
            opp_move = Strategy.sankalp_2(self.game, 'O')
            
        else:
            # 20% Column Stacker: Keeps the AI paranoid about vertical threats.
            opp_move = Strategy.column_stacker(self.game, 'O')

        # Fallback for safety
        if opp_move not in self.game.available_moves():
            opp_move = random.choice(self.game.available_moves())

        self.game.make_move(opp_move, 'O')

        if self.game.current_winner == 'O':
            return self._get_obs(), -1.0, True, False, {}  
        elif not self.game.available_moves():
            return self._get_obs(), 0.0, True, False, {}

        return self._get_obs(), 0.0, False, False, {}