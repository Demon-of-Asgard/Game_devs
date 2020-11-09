import pygame
import random

WIDTH  = 360
HEIGHT = 480
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
colors = [WHITE, BLACK, RED, GREEN, BLUE]

# Initialize pygame and create window.
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Game Loop
running = True
while running:
    # Keep loop running at right speed.
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update()
    # Draw/render
    all_sprites.draw(screen)
    color = colors[random.randint(0, len(colors)-1)]
    screen.fill(color)
    # After drawing everything
    pygame.display.flip()
