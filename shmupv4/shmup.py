#!/home/demon/.local/share/virtualenvs/shmup_base-VLPtn8i0/bin/python3

#-------------------------------------------------------------------------------
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
#-------------------------------------------------------------------------------


import os
import pygame, random 

#-------------------------------------------------------------------------------

from player.player import Player
from mob.mob import Mob
from bullets.bullets import Bullet
from explosion.explosion import Explosion 
from powerup.powerup import Powerup 

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

N_MOB = 3
#-------------------------------------------------------------------------------

asset_folder = os.path.join(os.path.dirname(__file__), 'img')
explosion_img_folder = os.path.join(os.path.dirname(__file__), 'explosion_img') 
powerup_img_folder = os.path.join(os.path.dirname(__file__), 'power-up_img')
sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

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
pygame.image.load(os.path.join(asset_folder, 'starfield_alpha.png')),
(SCREEN_WIDTH, SCREEN_HEIGHT)
)
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(asset_folder,
    'playerShip1_orange.png')).convert()
enemy_img  = pygame.image.load(os.path.join(asset_folder,
    'enemyBlue2.png')).convert()
bullet_img = pygame.image.load(os.path.join(asset_folder,
    'laserRed01.png')).convert()
enemy_bullet = pygame.image.load(os.path.join(asset_folder, 
'laserBlue08.png')).convert()

#-------------------------------------------------------------------------------

shoot_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'laser_gun.wav'))
enemy_explosion_sound  = pygame.mixer.Sound(os.path.join(sound_folder, '8bit_bomb_explosion.wav'))
pygame.mixer.music.load(os.path.join(sound_folder, 'FrozenJam_Loop.ogg'))
pygame.mixer.music.set_volume(0.05)

#-------------------------------------------------------------------------------

explosion_anim = {}
explosion_anim['kill'] = []
explosion_anim['hit'] = []

for i in range(4):
    kill_filename = 'expl0{}.png'.format(i)
    kill_img = pygame.image.load(os.path.join(explosion_img_folder, kill_filename)).convert()
    kill_img.set_colorkey(BLACK)
    kill_img = pygame.transform.scale(kill_img, (int(SCREEN_WIDTH/25), int(SCREEN_WIDTH/25)))
    explosion_anim['kill'].append(kill_img)

for i in range(4):
    hit_filename  = 'small_expl0{}.png'.format(i)
    hit_img = pygame.image.load(os.path.join(explosion_img_folder, hit_filename)).convert()
    hit_img.set_colorkey(BLACK)
    hit_img = pygame.transform.scale(hit_img, (int(SCREEN_WIDTH/60), int(SCREEN_WIDTH/60)))
    explosion_anim['hit'].append(hit_img)

#-------------------------------------------------------------------------------

powerup_img = {}
powerup_img['life'] = pygame.image.load(
    os.path.join(powerup_img_folder, 'powerup_star.png')
    ).convert()
powerup_img['bullet'] = pygame.image.load(
    os.path.join(powerup_img_folder, 'bullet_pack.png')
    ).convert()

#-------------------------------------------------------------------------------

all_sprites = pygame.sprite.Group()
mobs  = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
all_power = pygame.sprite.Group()
player = Player(player_img, bullet_img, SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

#-------------------------------------------------------------------------------

def spwan_mob():
    m = Mob(enemy_img, enemy_bullet, SCREEN_WIDTH, SCREEN_HEIGHT)
    mobs.add(m)
    all_sprites.add(m)

for i in range(N_MOB):
    spwan_mob()

#-------------------------------------------------------------------------------
def mob_shoot():
    mob_bullet = mob.shoot()
    enemy_bullets.add(mob_bullet)
    all_sprites.add(mob_bullet)

#-------------------------------------------------------------------------------

def explode(center, size):
    expl = Explosion(center, explosion_anim, size)
    all_sprites.add(expl)
    return expl 

#-------------------------------------------------------------------------------

def power_up():
    power = Powerup(powerup_img, SCREEN_WIDTH, SCREEN_HEIGHT)
    all_power.add(power)
    all_sprites.add(power)

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------

running = True
score = 0
pygame.mixer.music.play(loops = -1)

#-------------------------------------------------------------------------------

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.bullets > 0:
                    player.bullets -= 1
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if player.bullets > 0:
                    shoot_sound.play()


    all_sprites.update()
    
    kills = pygame.sprite.groupcollide(
        mobs, bullets,
        True, True
    )

    for kill in kills:
        # random.choice(explosion_sound).play()
        enemy_explosion_sound.play()
        explode(kill.rect.center, 'kill')
        score += 1
        spwan_mob()

    hits = pygame.sprite.spritecollide(
        player, mobs, True, 
        pygame.sprite.collide_circle
    )

    for hit in hits:
        player.life -= 1
        spwan_mob()
        explode(hit.rect.center, 'hit')
        if player.life <= 0:
            player.kill()
            death_expl = explode(hit.rect.center, 'kill')
            print("YOUR SCORE: {}".format(score))
    
    if not player.alive() and not death_expl.alive():
        running = False
        pygame.time.wait(500)

    power_lapse = random.randrange(20000, 30000)
    if player.now - player.last_powerup > power_lapse:
        player.last_powerup = player.now
        power_up()

    powerups = pygame.sprite.spritecollide(player, all_power, True, pygame.sprite.collide_circle)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    for powerup in powerups:
        if powerup.type == 'life':
            if player.life < player.life_max:
                player.life += 1
        
        if powerup.type == 'bullet':
            player.bullets += 50


    # for mob in mobs:``
    #     delay = random.randrange(1000, 2000)
    #     mob.now = pygame.time.get_ticks()
    #     if mob.now - mob.last_shoot  > delay:
    #         mob.last_shoot = mob.now
    #         mob_shoot()
            

    all_sprites.draw(screen)
    player.show_score(screen, 'Kills: '+str(score), 20, SCREEN_WIDTH-100, 20)

    if player.life <=1:
        life_color = RED
    else:
        life_color = GREEN
    player.show_life(screen,(player.life*100.0/player.life_max), life_color, 5,5)

    pygame.display.flip()

#-------------------------------------------------------------------------------
