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
            
        # Normal game start. 50% of the time, the opponent (O) goes first.
        if random.choice([True, False]) and self.game.available_moves():
            # Let the opponent make the first move
            self._play_opponent_move()
            
        return self._get_obs(), {}

    def _play_opponent_move(self):
        if not self.game.available_moves():
            return
            
        # Self-play: use the current RL model if available
        if hasattr(self, 'rl_model') and self.rl_model is not None:
            # Flip the board perspective: The model thinks it is 'X' (1.0)
            board_matrix = np.zeros((6, 7), dtype=np.float32)
            for r in range(6):
                for c in range(7):
                    piece = self.game.board[r][c]  
                    if piece == 'O':
                        board_matrix[r][c] = 1.0  # Opponent sees itself as 1
                    elif piece == 'X':
                        board_matrix[r][c] = -1.0 # Opponent sees us as -1
            obs = np.expand_dims(board_matrix, axis=0)
            
            action, _ = self.rl_model.predict(obs, deterministic=False)
            opp_move = int(action)
            
            # Fallback if the model predicts an invalid move
            if opp_move not in self.game.available_moves():
                opp_move = random.choice(self.game.available_moves())
        else:
            opp_move = random.choice(self.game.available_moves())
            
        self.game.make_move(opp_move, 'O')

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

        # === PURE SELF-PLAY ===
        self._play_opponent_move()

        if self.game.current_winner == 'O':
            return self._get_obs(), -1.0, True, False, {}  
        elif not self.game.available_moves():
            return self._get_obs(), 0.0, True, False, {}

        return self._get_obs(), 0.0, False, False, {}