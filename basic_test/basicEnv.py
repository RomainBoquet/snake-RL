import gym
from gym import spaces
import pygame
import random

class SimpleGameEnv(gym.Env):
    def __init__(self):
        super(SimpleGameEnv, self).__init__()
        self.width = 800
        self.height = 600
        self.player_width = 50
        self.player_height = 50
        self.obstacle_width = 50
        self.obstacle_height = 50
        self.player_x = 100
        self.player_y = self.height // 2 - self.player_height // 2
        self.obstacle_speed = 5
        self.obstacles = []
        self.clock = pygame.time.Clock()

        # Définir les espaces d'action et d'observation
        self.action_space = spaces.Discrete(2)  # 0: Haut, 1: Bas
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.width, self.height, 3), dtype=np.uint8)

    def reset(self):
        self.player_y = self.height // 2 - self.player_height // 2
        self.obstacles = []
        return self._get_obs()

    def step(self, action):
        if action == 0 and self.player_y - 5 >= 0:
            self.player_y -= 5
        elif action == 1 and self.player_y + 5 + self.player_height <= self.height:
            self.player_y += 5

        if random.randint(1, 20) == 1:
            obstacle_x = self.width
            obstacle_y = random.choice([0, self.height - self.obstacle_height])
            self.obstacles.append(pygame.Rect(obstacle_x, obstacle_y, self.obstacle_width, self.obstacle_height))

        for obstacle in self.obstacles:
            obstacle.x -= self.obstacle_speed
            if obstacle.x < 0:
                self.obstacles.remove(obstacle)

        done = self._check_collision()
        reward = -1 if done else 1
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        obs = pygame.surfarray.array3d(pygame.display.set_mode((self.width, self.height)))
        return obs

    def _check_collision(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle):
                return True
        return False

    def render(self, mode='human'):
        pygame.init()
        win = pygame.display.set_mode((self.width, self.height))
        win.fill((255, 255, 255))
        pygame.draw.rect(win, (0, 0, 0), (self.player_x, self.player_y, self.player_width, self.player_height))
        for obstacle in self.obstacles:
            pygame.draw.rect(win, (255, 0, 0), obstacle)
        pygame.display.update()

    def close(self):
        pygame.quit()

