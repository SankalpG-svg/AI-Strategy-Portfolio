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


# 1. Direct fix for your Windows TensorBoard locking issue
os.makedirs("./tensorboard_logs/", exist_ok=True)

# 2. Load the previous model to act as the self-play opponent
best_model_path = "custom_connect4_cnn.zip" # update with your actual checkpoint file name
opp_model = None

if os.path.exists(best_model_path):
    print(f"--- Loading {best_model_path} for Self-Play Curriculum ---")
    opp_model = PPO.load(best_model_path)

# 3. Instantiate environment with the self-play opponent
env = ConnectFourGym(opponent_model=opp_model)

# 4. Define or Load the Training Model
if opp_model is not None:
    model = PPO.load(
        best_model_path, 
        env=env, 
        tensorboard_log="./tensorboard_logs/",
        custom_objects={
            "gamma": 0.95,
            "learning_rate": 3e-4
        }
    )
else:
    # Hyperparameter tuning to stop lazy behaviors
    model = PPO(
        "CnnPolicy", 
        env, 
        verbose=1, 
        tensorboard_log="./tensorboard_logs/",
        gamma=0.95,       # Lower gamma pushes the model to value immediate wins over future wins
        learning_rate=3e-4
    )

checkpoint_callback = CheckpointCallback(
    save_freq=20000, 
    save_path="./checkpoints/", 
    name_prefix="c4_ppo_model"
)

# 5. Run the Bake
print("Starting training session...")
model.learn(total_timesteps=200000, callback=checkpoint_callback)
model.save("custom_connect4_cnn")