import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from connect_four import ConnectFour 
from strategy_c4 import Strategy

class ConnectFourGym(gym.Env):
    def __init__(self, opponent_model=None):
        super(ConnectFourGym, self).__init__()
        self.game = ConnectFour()
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            low=-1.0, 
            high=1.0, 
            shape=(1, 6, 7), 
            dtype=np.float32
        )
        # Self-play infrastructure: allows passing a trained PPO model as an opponent
        self.opponent_model = opponent_model

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = ConnectFour()
        
        if hasattr(Strategy, '_target_col'):
            delattr(Strategy, '_target_col')

        # === MID-GAME CLUTTER ===
        if random.random() < 0.50:
            for _ in range(random.randint(2, 6)):
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
                if self.game.board[0][threat_col] == ' ':
                    self.game.make_move(threat_col, 'O')
                    self.game.make_move(threat_col, 'O')
                    self.game.make_move(threat_col, 'O')
                    Strategy._target_col = threat_col 
                
            elif trap_type == "horizontal":
                start_col = random.randint(1, 3)
                if self.game.board[5][start_col] == ' ':
                    self.game.make_move(start_col, 'O')
                    self.game.make_move(start_col + 1, 'O')
                    self.game.make_move(start_col + 2, 'O')
                    Strategy._target_col = random.choice([start_col - 1, start_col + 3])
                
            return self._get_obs(), {}
            
        if random.choice([True, False]) and self.game.available_moves():
            opp_move = random.choice(self.game.available_moves())
            self.game.make_move(opp_move, 'O')
            
        return self._get_obs(), {}

    def _get_obs(self):
        board_matrix = np.zeros((6, 7), dtype=np.float32)
        for r in range(6):
            for c in range(7):
                piece = self.game.board[r][c]  
                if piece == 'X':
                    board_matrix[r][c] = 1.0
                elif piece == 'O':
                    board_matrix[r][c] = -1.0
                    
        return np.expand_dims(board_matrix, axis=0)

    def step(self, action):
        if action not in self.game.available_moves():
            # Heavy penalty for illegal moves
            return self._get_obs(), -10.0, True, False, {}

        # 1. The AI (X) plays its turn
        self.game.make_move(action, 'X')

        if self.game.current_winner == 'X':
            return self._get_obs(), 1.0, True, False, {}  
        elif not self.game.available_moves():
            return self._get_obs(), 0.0, True, False, {}

        # 2. Opponent Selection Logic (Curriculum)
        roll = random.randint(1, 100)
        
        # If a self-play model is provided, use it 40% of the time to counter human style traps
        if self.opponent_model is not None and roll <= 40:
            # Predict expects an observation matching player 'O' perspective (flip the signs)
            opp_obs = -self._get_obs() 
            opp_move, _ = self.opponent_model.predict(opp_obs, deterministic=True)
            opp_move = int(opp_move)
        else:
            # Algorithmic Bot Pool
            sub_roll = random.randint(1, 100)
            if sub_roll <= 60:
                # Upgraded to your fast alpha-beta minimax bot (Depth 4)
                opp_move = Strategy.kaggle_minimax(self.game, 'O', depth=4)
            elif sub_roll <= 85:
                opp_move = Strategy.sankalp_2(self.game, 'O')
            else:
                opp_move = Strategy.column_stacker(self.game, 'O')

        # Fallback safety
        if opp_move not in self.game.available_moves():
            opp_move = random.choice(self.game.available_moves())

        # 3. Opponent plays its turn
        self.game.make_move(opp_move, 'O')

        if self.game.current_winner == 'O':
            return self._get_obs(), -2.5, True, False, {}  
        elif not self.game.available_moves():
            return self._get_obs(), 0.0, True, False, {}

        # === REWARD SHAPING: Step Penalty ===
        # Small penalty every turn encourages finishing the game as fast as possible
        return self._get_obs(), -0.02, False, False, {}