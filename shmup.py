import os
import random
import pygame
import numpy
import math
#-------------------------------------------------------------------------------
# SCREEN_HEIGHT = 700
# SCREEN_WIDTH  = 700
FPS = 90

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
SCALE_WIDTH   = 1.0/30.0
SCALE_LENGTH  = 1.0/10.0
LENGTH_BUFFER = 10
WIDTH_BUFFER  = 5
ENEMY_SPEED_SCALEX = 1.0
ENEMY_SPEED_SCALEY = 1.0/50.0

#-------------------------------------------------------------------------------

asset_folder = os.path.join(os.path.dirname(__file__), 'img')
#-------------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shmup!')
clock  = pygame.time.Clock()
#-------------------------------------------------------------------------------

background = pygame.transform.scale(pygame.image.load(os.path.join(asset_folder, 'starfield_alpha.png')),(SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(asset_folder, 'playerShip1_orange.png')).convert()
enemy_img  = pygame.image.load(os.path.join(asset_folder, 'enemyBlue2.png')).convert()
bullet_img = pygame.image.load(os.path.join(asset_folder, 'bullet2.png')).convert()

#-------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.scale = (int(SCREEN_WIDTH*SCALE_WIDTH*1.2), int(SCREEN_HEIGHT*SCALE_LENGTH*1.2))
        self.image_orig = pygame.transform.scale(player_img, self.scale)
        self.image = self.image_orig.copy()
        self.rect  = self.image.get_rect()
        self.radius = int(self.scale[0]/2.0)
        self.image.set_colorkey(BLACK)
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.bottom  = SCREEN_HEIGHT-10

        self.head = 'up'
        self.speedx = 0
        self.speedy = 0
        self.rot = 0
        self.rot_speed = 90


    def update(self):
        self.move()


    def move(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -int(SCREEN_WIDTH*SCALE_WIDTH)
            self.rect.x += self.speedx


        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = int(SCREEN_WIDTH*SCALE_WIDTH)
            self.rect.x += self.speedx

        if ((keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and
        (keystate[pygame.K_RIGHT] or keystate[pygame.K_d])):
            self.speedx = 0
            self.rect.x += self.speedx



        if self.rect.left   < WIDTH_BUFFER:
            self.rect.left  = WIDTH_BUFFER
        if self.rect.right  > SCREEN_WIDTH-WIDTH_BUFFER:
            self.rect.right = SCREEN_WIDTH-WIDTH_BUFFER

        self.speedy = 0

        if keystate[pygame.K_UP]:
            self.speedy = -int(SCREEN_HEIGHT*SCALE_LENGTH)
            self.rect.y += self.speedy


        if keystate[pygame.K_DOWN]:
            self.speedy = int(SCREEN_HEIGHT*SCALE_LENGTH)
            self.rect.y += self.speedy

        if self.rect.top < LENGTH_BUFFER:
            self.rect.top = int(SCALE_LENGTH)
        if self.rect.bottom > SCREEN_HEIGHT - LENGTH_BUFFER:
            self.rect.bottom = int(SCREEN_HEIGHT -LENGTH_BUFFER)


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
#-------------------------------------------------------------------------------

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.scale = (int(SCREEN_WIDTH*SCALE_WIDTH), int(SCREEN_HEIGHT*SCALE_LENGTH))
        self.speedy = random.randrange(int(SCREEN_HEIGHT*ENEMY_SPEED_SCALEY/2.0), int(SCREEN_HEIGHT*2*ENEMY_SPEED_SCALEY))
        self.speedx = random.randrange(-int(SCREEN_WIDTH*ENEMY_SPEED_SCALEX), int(SCREEN_WIDTH*ENEMY_SPEED_SCALEX))

        self.speedr = math.sqrt(self.speedx**2+self.speedy**2)

        if self.speedx <= 0:
            self.head = -int(math.acos(self.speedy/self.speedr)*(180.0/math.pi))
        if self.speedx > 0:
            self.head = int(math.acos(self.speedy/self.speedr)*(180.0/math.pi))


        self.image_orig = pygame.transform.scale(enemy_img, self.scale)
        new_image = pygame.transform.rotate(self.image_orig,self.head)

        self.image = new_image.copy()
        self.rect  = self.image.get_rect()
        self.radius = int(self.scale[0]/2.0)
        self.image.set_colorkey(BLACK)
        self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25):

            self.speedy = random.randrange(int(SCREEN_HEIGHT*ENEMY_SPEED_SCALEY/2.0), int(SCREEN_HEIGHT*2*ENEMY_SPEED_SCALEY))
            self.speedx = random.randrange(-int(SCREEN_WIDTH*ENEMY_SPEED_SCALEX), int(SCREEN_WIDTH*ENEMY_SPEED_SCALEX))

            self.speedr = math.sqrt(self.speedx**2+self.speedy**2)

            if self.speedx <= 0:
                self.head = -int(math.acos(self.speedy/self.speedr)*(180.0/math.pi))
            if self.speedx > 0:
                self.head = int(math.acos(self.speedy/self.speedr)*(180.0/math.pi))
            new_image = pygame.transform.rotate(self.image_orig, self.head)

            self.image = new_image
            self.rect  = self.image.get_rect()
            self.image.set_colorkey(BLACK)

            self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100, -40)

#-------------------------------------------------------------------------------

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(bullet_img, (15, 50))
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = -int(SCREEN_HEIGHT*SCALE_LENGTH*.5)

    def update(self):
        self.rect.y += self.speedy

        if (self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.top > SCREEN_HEIGHT or self.rect.right < 0):
            self.kill()
#-------------------------------------------------------------------------------

all_sprites = pygame.sprite.Group()
mobs  = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(5):
    m = Mob()
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
                player.shoot()

    all_sprites.update()

    kills = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for kill in kills:
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    if hits:
        running = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
#-------------------------------------------------------------------------------
