import pygame
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces

class SnakeEnv(gym.Env):
    def __init__(self, grid_size=10, render_mode=None):
        self.grid_size = grid_size
        self.cell_size = 20
        self.render_mode = render_mode

        # Actions possibles: [0=haut, 1=bas, 2=gauche, 3=droite]
        self.action_space = spaces.Discrete(4)
        
        # Observations: grille (1 canal, grid_size x grid_size)
        # Ajoutez une dimension pour la compatibilité CNN
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(self.grid_size, self.grid_size, 3), dtype=np.float32
        )

        # Initialisation du jeu
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        """Réinitialise le jeu et retourne l'état initial."""
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]  # Serpent au centre
        self.direction = (0, 1)  # Direction initiale (droite)
        self.food = self._place_food()  # Place la nourriture
        self.done = False
        self.score = 0

        return self._get_observation(), {}

    def step(self, action):
        """
        Exécute une action et retourne (new_state, reward, done, info).
        """
        # Mise à jour de la direction
        self._update_direction(action)

        # Calcul de la nouvelle position de la tête
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Initialisation de reward à une valeur par défaut
        reward = 0.  # Récompense mineure pour un déplacement (optionnel)
        self.done = False

        previous_distance = self._distance_to_food(self.snake[0])
        new_distance = self._distance_to_food(new_head)

        if new_distance < previous_distance:
            reward += 1  # Récompense pour se rapprocher de la nourriture
        elif new_distance > previous_distance:
            reward -= 1  # Pénalité pour s'éloigner



        # Vérifier les collisions
        if (
            new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake
        ):
            self.done = True
            reward = -10  # Récompense négative pour collision
            return self._get_observation(), reward, self.done, False, {}

        # Mise à jour du serpent
        self.snake.insert(0, new_head)
        if new_head == self.food:
            reward = 10  # Récompense pour avoir mangé la nourriture
            self.food = self._place_food()  # Placer une nouvelle nourriture
            self.score += 1
        else:
            reward = -0.1  # Small negative reward for each step taken
            self.snake.pop()  # Retirer la queue pour garder la taille

        # Additional reward shaping
        if abs(new_head[0] - self.food[0]) + abs(new_head[1] - self.food[1]) < abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1]):
            reward += 0.1  # Small positive reward for moving closer to the food

        # Retourner l'état
        return self._get_observation(), reward, self.done, False, {}

    def render(self, mode="human"):
        """Affiche ou retourne l'état de l'environnement."""
        screen_size = self.grid_size * self.cell_size
        if self.render_mode == "rgb_array":
            # Return an RGB array representation of the environment
            return np.zeros((self.grid_size, self.grid_size, 3), dtype=np.uint8)
        elif mode == "human":
            pygame.init()
            screen = pygame.display.set_mode((screen_size, screen_size))
            screen.fill((0, 0, 0))

            # Dessine le serpent
            for segment in self.snake:
                rect = pygame.Rect(
                    segment[1] * self.cell_size, segment[0] * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, (0, 255, 0), rect)

            # Dessine la nourriture
            rect = pygame.Rect(
                self.food[1] * self.cell_size, self.food[0] * self.cell_size,
                self.cell_size, self.cell_size
            )
            pygame.draw.rect(screen, (255, 0, 0), rect)

            pygame.display.flip()

        else:
            raise ValueError(f"Mode de rendu non supporté : {mode}")


    def _place_food(self):
        """Place la nourriture à un endroit aléatoire."""
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                return food

    def _distance_to_food(self, position):
        """Calcule la distance de Manhattan entre une position donnée et la nourriture."""
        return abs(position[0] - self.food[0]) + abs(position[1] - self.food[1])

    def _update_direction(self, action):
        """Met à jour la direction en fonction de l'action."""
        if action == 0 and self.direction != (1, 0):  # Haut
            self.direction = (-1, 0)
        elif action == 1 and self.direction != (-1, 0):  # Bas
            self.direction = (1, 0)
        elif action == 2 and self.direction != (0, 1):  # Gauche
            self.direction = (0, -1)
        elif action == 3 and self.direction != (0, -1):  # Droite
            self.direction = (0, 1)

    def _get_observation(self):
        """Génère une observation représentant l'état actuel de la grille."""
        return np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)