#-------------------------------------------------------------------------------
import os
import pygame
#-------------------------------------------------------------------------------
from player.player import Player
from mob.mob import Mob
from bullets.bullets import Bullet

#-------------------------------------------------------------------------------

FPS = 90

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)

SCALE_WIDTH   = 1.0/25.0
SCALE_LENGTH  = 1.0/12.0

Y_BUFFER = 10
X_BUFFER  = 5

ENEMY_SPEED_SCALEX = 1.0/150.0
ENEMY_SPEED_SCALEY = 1.0/100.0
#-------------------------------------------------------------------------------

asset_folder = os.path.join(os.path.dirname(__file__), 'img')
#-------------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH  = pygame.display.Info().current_w
SCREEN_HEIGHT  = pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shmup!')
clock  = pygame.time.Clock()
#-------------------------------------------------------------------------------

background = pygame.transform.scale(
pygame.image.load(os.path.join(asset_folder, 'black.png')),
(SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(asset_folder,
'playerShip1_orange.png')).convert()
enemy_img  = pygame.image.load(os.path.join(asset_folder,
'enemyBlue2.png')).convert()
bullet_img = pygame.image.load(os.path.join(asset_folder,
'bullet2.png')).convert()

#-------------------------------------------------------------------------------

all_sprites = pygame.sprite.Group()
mobs  = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(player_img, bullet_img, SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

for i in range(5):
    m = Mob(enemy_img, SCREEN_WIDTH, SCREEN_HEIGHT)
    mobs.add(m)
    all_sprites.add(m)

running = True

#-------------------------------------------------------------------------------
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot_L()
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullet = player.shoot_R()
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()

    kills = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for kill in kills:
        m = Mob(enemy_img, SCREEN_WIDTH, SCREEN_HEIGHT)
        mobs.add(m)
        all_sprites.add(m)

    hits = pygame.sprite.spritecollide(
    player, mobs, False,
    pygame.sprite.collide_circle
    )

    if hits:
        running = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
#-------------------------------------------------------------------------------
