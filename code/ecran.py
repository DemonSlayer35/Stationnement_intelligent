import pygame

# Initialiser Pygame
pygame.init()

liste = [0] * 18

# Définir la taille de l'écran
screen_width = 1152
screen_height = 648
screen = pygame.display.set_mode((screen_width, screen_height))

# Remplir l'écran avec du noir
screen.fill((0, 0, 0))

# Définir la taille et la position des rectangles
rect_width = screen_width // 10
rect_height = screen_height // 3
rect_x = 37
rect_y = 54

# Dessiner les cadres des rectangles blancs et numéroter les places
font = pygame.font.Font(None, 36)
for i in range(18):
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    if liste[i] == 0:
        pygame.draw.rect(screen, (0, 255, 0), rect)
    elif liste[i] == 1:
        pygame.draw.rect(screen, (255, 0, 0), rect)
    if i < 9:
        place_num = str(i - 8 + 18)
    else:
        place_num = str(18 - i)
    place_text = font.render(place_num, 1, (255, 255, 255))
    text_x = rect_x + rect_width // 2 - place_text.get_width() // 2
    text_y = rect_y + rect_height // 2 - place_text.get_height() // 2
    screen.blit(place_text, (text_x, text_y))
    rect_x += rect_width + 5
    if (i + 1) % 9 == 0:
        rect_x = 37
        rect_y += rect_height + rect_height // 2

# Mettre à jour l'affichage
pygame.display.update()

# Boucle principale de l'application
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quitter Pygame
pygame.quit()