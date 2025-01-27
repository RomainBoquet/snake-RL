import pygame
import sys
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la grille
grid_size = 20
cell_size = 20
screen_size = grid_size * cell_size

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (100, 100, 100)

# Création de la fenêtre
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake Game")

# Initialisation des variables globales
def reset_game():
    global snake, direction, food, score
    snake = [(10, 10), (9, 10), (8, 10)]  # Liste de segments de serpent (x, y)
    direction = (1, 0)  # Direction initiale (droite)
    food = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    score = 0

reset_game()

# Police pour le texte
font = pygame.font.Font(None, 36)

# Fonction pour dessiner la grille
def draw_grid():
    for x in range(0, screen_size, cell_size):
        for y in range(0, screen_size, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, white, rect, 1)

# Fonction pour dessiner le serpent
def draw_snake(snake):
    for segment in snake:
        rect = pygame.Rect(segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, green, rect)

# Fonction pour dessiner la nourriture
def draw_food(food):
    rect = pygame.Rect(food[0] * cell_size, food[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, red, rect)

# Fonction pour afficher le score
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

# Fonction pour mettre à jour la position du serpent
def update_snake(snake, direction, food):
    # Calculer la nouvelle position de la tête
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)  # Ajouter la nouvelle tête

    # Vérifier si le serpent mange la nourriture
    if new_head == food:
        return True  # La nourriture a été mangée
    else:
        snake.pop()  # Retirer la queue pour garder la même longueur
        return False

# Fonction pour détecter les collisions
def check_collisions(snake):
    head = snake[0]
    # Collision avec les murs
    if head[0] < 0 or head[0] >= grid_size or head[1] < 0 or head[1] >= grid_size:
        return True
    # Collision avec le corps du serpent
    if head in snake[1:]:
        return True
    return False

# Fonction pour afficher l'écran de fin de jeu
def game_over_screen(score):
    screen.fill(black)
    game_over_text = font.render("Game Over", True, red)
    score_text = font.render(f"Final Score: {score}", True, white)
    restart_button = pygame.Rect(screen_size // 4, screen_size // 2, screen_size // 2, 50)
    quit_button = pygame.Rect(screen_size // 4, screen_size // 2 + 70, screen_size // 2, 50)

    screen.blit(game_over_text, (screen_size // 2 - game_over_text.get_width() // 2, screen_size // 3))
    screen.blit(score_text, (screen_size // 2 - score_text.get_width() // 2, screen_size // 3 + 40))
    pygame.draw.rect(screen, gray, restart_button)
    pygame.draw.rect(screen, gray, quit_button)

    restart_text = font.render("Restart", True, black)
    quit_text = font.render("Quit", True, black)
    screen.blit(restart_text, (restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2, restart_button.y + 10))
    screen.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + 10))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"  # Retourner le choix de redémarrage
                elif quit_button.collidepoint(event.pos):
                    return "quit"  # Retourner le choix de quitter

# Boucle principale
def main():
    global direction, food, score

    while True:
        reset_game()
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)

            # Mise à jour de la position du serpent
            ate_food = update_snake(snake, direction, food)

            # Générer une nouvelle nourriture si elle est mangée
            if ate_food:
                score += 1
                food = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

            # Vérifier les collisions
            if check_collisions(snake):
                running = False

            # Mise à jour de l'affichage
            screen.fill(black)  # Efface l'écran
            draw_grid()
            draw_snake(snake)
            draw_food(food)
            draw_score(score)
            pygame.display.flip()

            clock.tick(6)  # Limite la vitesse à 10 FPS

        # Afficher l'écran de fin de jeu
        choice = game_over_screen(score)
        if choice == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
