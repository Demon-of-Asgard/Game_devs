import pygame
import random
import os

HEIGHT = 600
WIDTH  = 400
FPS    = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

game_folder = os.path.dirname(__file__)
img_folder  = os.path.join(game_folder, 'img')

class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.states = {
            "stationary": os.path.join(img_folder, 'firefox.png'),
            "flying"    : os.path.join(img_folder, 'firefox_flying.png'),
            "landing"   : os.path.join(img_folder, 'firefox_landing.png')
        }

        self.render_state = self.states["stationary"]
        self.image = pygame.image.load(self.render_state).convert()

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (int(0), int(HEIGHT/2.0))
        self.y_speed = 1


    def update(self):
        self.rect.x += 1
        self.rect.y += self.y_speed
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom >= HEIGHT-200:
            self.y_speed = -self.y_speed
            self.render_state = self.states['flying']
        if self.rect.top <= 200:
            self.y_speed = -self.y_speed
            self.render_state = self.states['landing']

        self.image = pygame.image.load(self.render_state).convert()
        self.image.set_colorkey(BLACK)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("My Game")

clock  = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
