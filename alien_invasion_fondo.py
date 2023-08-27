import pygame
import random
from ship import Ship
import settings_nueva  # Importa los valores de configuración desde settings.py

pygame.init()

# Inicializa la ventana
screen = pygame.display.set_mode((settings_nueva.screen_width, settings_nueva.screen_height))
pygame.display.set_caption("Alien Invasion 8 Bits")

def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, settings_nueva.screen_width)
        y = random.randint(0, settings_nueva.screen_height)
        stars.append((x, y))
    return stars

def draw_stars(stars):
    for star in stars:
        x, y = star
        pygame.draw.circle(screen, settings_nueva.white, (x, y), 1)

clock = pygame.time.Clock()

running = True

stars = create_stars(settings_nueva.num_stars)  # Usa el número de estrellas desde settings.py

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(settings_nueva.black)
    draw_stars(stars)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()