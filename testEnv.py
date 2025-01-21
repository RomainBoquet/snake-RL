from SnakeEnv import SnakeEnv
import time


env = SnakeEnv()

state = env.reset()
done = False

while not done:
    action = env.action_space.sample()  # Action aléatoire
    print(action)

    state, reward, done, info = env.step(action)

    env.render()
    time.sleep(0.1)
    print(reward)

env.close()