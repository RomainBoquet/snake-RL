from stable_baselines3 import PPO
from SnakeEnv import SnakeEnv
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

# Create a vectorized environment
env = DummyVecEnv([lambda: SnakeEnv(grid_size=10, render_mode='rgb_array') for _ in range(4)])

# Optionally, record videos of the agent's performance
env = VecVideoRecorder(env, "videos/", record_video_trigger=lambda x: x % 10000 == 0, video_length=200)

model = PPO("MlpPolicy",
            env,
            learning_rate=1e-3,
            n_steps=2048,
            batch_size=64,
            verbose=2)

# Train the agent
model.learn(total_timesteps=100000)

# Save the model
model.save('models/model_lr_1e-3_timestep_100000')