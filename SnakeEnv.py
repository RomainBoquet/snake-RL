import pygame
import random
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box

class SnakeEnv(Env):
    def __init__(self, grid_size=20):
        super(SnakeEnv, self).__init__()
        self.grid_size = grid_size
        self.cell_size = 20

        # Actions possibles: [0=haut, 1=bas, 2=gauche, 3=droite]
        self.action_space = Discrete(4)
        
        # Observations: grille (matrice 2D avec état du jeu)
        # 0 = vide, 1 = mur, 2 = nourriture, 3 = corps du serpent
        self.observation_space = Box(
            low=0, high=3, shape=(self.grid_size, self.grid_size), dtype=np.uint8
        )

        # Initialisation du jeu
        self.reset()

    def reset(self):
        """Réinitialise le jeu et retourne l'état initial."""
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]  # Serpent au centre
        self.direction = (0, 1)  # Direction initiale (droite)
        self.food = self._place_food()  # Place la nourriture
        self.done = False
        self.score = 0

        return self._get_observation()

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
            return self._get_observation(), reward, self.done, {}

        # Mise à jour du serpent
        self.snake.insert(0, new_head)
        if new_head == self.food:
            reward = 10  # Récompense pour avoir mangé la nourriture
            self.food = self._place_food()  # Placer une nouvelle nourriture
            self.score += 1
        else:
            self.snake.pop()  # Retirer la queue pour garder la taille

        # Retourner l'état
        return self._get_observation(), reward, self.done, {}


    def render(self, mode="human"):
        """Affiche l'environnement à l'écran."""
        pygame.init()
        screen_size = self.grid_size * self.cell_size
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
        grid = np.zeros((self.grid_size, self.grid_size), dtype=np.uint8)

        # Ajoute les murs (facultatif)
        # grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 1

        # Ajoute le serpent
        for x, y in self.snake:
            grid[x, y] = 3

        # Ajoute la nourriture
        food_x, food_y = self.food
        grid[food_x, food_y] = 2

        return grid