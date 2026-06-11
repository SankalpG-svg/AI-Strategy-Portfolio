import os
import gymnasium as gym
import torch as th
import torch.nn as nn
from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.callbacks import CheckpointCallback
from gym_env import ConnectFourGym

# 1. The Custom Kaggle CNN Extractor
class CustomCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 128):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        n_input_channels = observation_space.shape[0]
        
        self.cnn = nn.Sequential(
            # FIX: Changed padding=0 to padding=1 to cure Edge Blindness!
            nn.Conv2d(n_input_channels, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Calculate exact shape using a dummy pass
        with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        self.linear = nn.Sequential(
            nn.Linear(n_flatten, features_dim), 
            nn.ReLU()
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))

# 2. Tell PPO to swap its default network design with our Custom CNN
policy_kwargs = dict(
    features_extractor_class=CustomCNN,
)

# 3. Create backup folders
os.makedirs("./models/", exist_ok=True)
checkpoint_callback = CheckpointCallback(
    save_freq=50_000,
    save_path="./models/",
    name_prefix="rl_kaggle_cnn_backup"
)

# 4. Initialize and Run
print("Starting environment with spatial channel layout...")
env = ConnectFourGym()

# COMPLETELY DELETED THE PPO(...) CREATION BLOCK

print("Waking up the 185k Master Brain...")
# LOAD THE BRAIN AND TELL IT WHERE TO DRAW GRAPHS SIMULTaneously
model = PPO.load(
    "custom_connect4_cnn", 
    env=env,
    tensorboard_log="./tensorboard_logs/"  # <--- CRITICAL FOR TENSORBOARD
)

print("Beginning Multi-Threat & Mid-Game learning...")
model.learn(total_timesteps=100000, callback=checkpoint_callback)

print("Saving the true spatial master model...")
model.save("custom_connect4_cnn")