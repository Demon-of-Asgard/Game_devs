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
from text.text import Text

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
pygame.image.load(os.path.join(asset_folder, 'starfield.png')),
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

for i in range(9):
    kill_filename = 'regularExplosion0{}.png'.format(i)
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
    os.path.join(powerup_img_folder, 'laserRed09.png')
    ).convert()
powerup_img['bullet'] = pygame.image.load(
    os.path.join(powerup_img_folder, 'bullet_pack.png')
    ).convert()

#-------------------------------------------------------------------------------
TextObj = Text() 
def show_gameover_screen():
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    TextObj.draw_text(screen, 'SHMUP!', int(SCREEN_WIDTH/2)-100, int(SCREEN_HEIGHT/4), 50)
    info = 'Arrow keys to manuver, space to shoot'
    TextObj.draw_text(screen, info, int(SCREEN_WIDTH/2)-200, int(SCREEN_HEIGHT/2), 25)
    TextObj.draw_text(screen, 'Press a key to begin', int(SCREEN_WIDTH/2)-100, int(SCREEN_HEIGHT/1.5), 18)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            


#-------------------------------------------------------------------------------

def spwan_mob():
    m = Mob(enemy_img, enemy_bullet, SCREEN_WIDTH, SCREEN_HEIGHT)
    return m

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

game_over = True
running = True
pygame.mixer.music.play(loops = -1)

#-------------------------------------------------------------------------------

while running:
    
    if game_over:
        show_gameover_screen()
        game_over = False 
        score = 0

        all_sprites = pygame.sprite.Group()
        mobs  = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        all_power = pygame.sprite.Group()
        player = Player(player_img, bullet_img, SCREEN_WIDTH, SCREEN_HEIGHT)
        all_sprites.add(player)

        player.last_powerup = player.now


        for i in range(N_MOB):
            m = spwan_mob()
            mobs.add(m)
            all_sprites.add(m)

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
        m = spwan_mob()
        mobs.add(m)
        all_sprites.add(m)

    hits = pygame.sprite.spritecollide(
        player, mobs, True, 
        pygame.sprite.collide_circle
    )

    for hit in hits:
        player.life -= 1
        explode(hit.rect.center, 'hit')
        m = spwan_mob()
        mobs.add(m)
        all_sprites.add(m)

        if player.life <= 0:
            player.kill()
            death_expl = explode(hit.rect.center, 'kill')
            print("YOUR SCORE: {}".format(score))
    
    if not player.alive() and not death_expl.alive():
        game_over = True
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
                player.last_powerup = pygame.time.get_ticks()
        
        if powerup.type == 'bullet':
            player.bullets += 50
            player.last_powerup = pygame.time.get_ticks()

    all_sprites.draw(screen)
    player.show_score(screen, 'Kills: '+str(score), 20, SCREEN_WIDTH-100, 20)

    if player.life <=1:
        life_color = RED
    else:
        life_color = GREEN
    player.show_life(screen,(player.life*100.0/player.life_max), life_color, 5,5)

    pygame.display.flip()

#-------------------------------------------------------------------------------
