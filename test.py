import time
from stable_baselines3 import PPO
from SnakeEnv import SnakeEnv

model = PPO.load("models/ppo_snake_model_cnn")
env = SnakeEnv(grid_size=10)

for episode in range(100): 
    obs = env.reset()
    done = False
    cumulative_reward = 0

    while not done:
        # Get the action from the model
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)  # Take a step in the environment
        cumulative_reward += reward

        # Optional: Add a delay to slow down rendering for visualization
        # time.sleep(0.1)
        # env.render()


    print(f"Episode {episode + 1}: Cumulative Reward = {cumulative_reward}")

env.close()
print("Tests terminés!")
