import time
from stable_baselines3 import PPO
from SnakeEnv import SnakeEnv
from stable_baselines3.common.vec_env import DummyVecEnv

# Load the trained model
model = PPO.load('models/model_lr_1e-3_timestep_100000')

# Create the environment
env = DummyVecEnv([lambda: SnakeEnv(grid_size=10, render_mode='human')])

# Reset the environment
obs = env.reset()

cumulative_reward = 0
done = False

while not done:
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)  # Take a step in the environment
    cumulative_reward += reward

    # Optional: Add a delay to slow down rendering for visualization
    time.sleep(0.1)
    env.render()

env.close()
print(cumulative_reward)
print("Tests terminés!")
