from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from basicEnv import SimpleGameEnv


env = SimpleGameEnv()
vec_env = make_vec_env(lambda: env, n_envs=1)

model = PPO('CnnPolicy', vec_env, verbose=1)
model.learn(total_timesteps=10000)
print("Training complete!")

obs = vec_env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    # vec_env.render()

print(rewards, dones, info)