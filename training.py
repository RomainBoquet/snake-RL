from stable_baselines3 import PPO
from SnakeEnv import SnakeEnv

# Créez l'environnement
env = SnakeEnv(grid_size=15)

# Créez un agent PPO
model = PPO("MlpPolicy", env, verbose=1)

# Entraînez l'agent
model.learn(total_timesteps=10000)