from stable_baselines3 import PPO
from SnakeEnv import SnakeEnv
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

# env = DummyVecEnv([lambda: SnakeEnv(grid_size=10)])
# env = VecVideoRecorder(env, "videos/", record_video_trigger=lambda x: x % 100 == 0, video_length=200)

env = SnakeEnv(grid_size=10)

model = PPO("MlpPolicy",
            env,
            learning_rate=1e-3,
            n_steps=2048,
            batch_size=64,
            verbose=2)

# Entraînez l'agent
model.learn(total_timesteps=100000)

model.save('models/model_lr_1e-3_timestep_100000')