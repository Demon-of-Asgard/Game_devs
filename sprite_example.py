import pygame
import random

WIDTH  = 380
HEIGHT = 500
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
colors = [WHITE, BLACK, RED, GREEN, BLUE]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(25, 25)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH/2.), int(HEIGHT/2.))

# Initialize pygame and create window.
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # After drawing everything
    pygame.display.flip()
