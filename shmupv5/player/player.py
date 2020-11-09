import pygame
import numpy
from bullets.bullets import Bullet

#-------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, bullet_img, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.SCALE_WIDTH  = 1.0/35.0
        self.SCALE_LENGTH = 1.0/17.0
        self.BULLET_SCALE = (1.0/200.0, 1.0/25.0)
        self.Y_BUFFER  = 10
        self.X_BUFFER  = 5
        self.BLACK = (0, 0, 0)
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        self.direction = 'up'

        self.scale = (
            int(self.SCREEN_WIDTH*self.SCALE_WIDTH),
            int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
        )

        self.image_orig  = pygame.transform.scale(player_img, self.scale)
        self.bullet_image_orig = pygame.transform.scale(bullet_img, 
            (int(self.SCREEN_WIDTH*self.BULLET_SCALE[0]),
            int(self.SCREEN_HEIGHT*self.BULLET_SCALE[1]))
            )

        self.image_up    = self.image_orig.copy()
        self.image_down  = self.image_orig.copy()
        self.image_left  = self.image_orig.copy()
        self.image_right = self.image_orig.copy()

        self.image_down  = pygame.transform.rotate(self.image_down, 180)
        self.image_left  = pygame.transform.rotate(self.image_left, 90)
        self.image_right = pygame.transform.rotate(self.image_right, -90)

        self.bullet_img_top    = self.bullet_image_orig.copy()
        self.bullet_img_left   = pygame.transform.rotate(self.bullet_image_orig, 90)
        self.bullet_img_right  = pygame.transform.rotate(self.bullet_image_orig, -90)
        self.bullet_img_bottom = pygame.transform.rotate(self.bullet_image_orig, 180)

        self.bullet_img = self.bullet_img_top 
        
        self.image = self.image_up
        self.rect  = self.image.get_rect()

        self.radius = int(
            (1.0/4.0)*numpy.sqrt(self.scale[0]**2+self.scale[1]**2)
        )

        self.image.set_colorkey(self.BLACK)
        self.rect.centerx = int(self.SCREEN_WIDTH/2)
        self.rect.bottom  = self.SCREEN_HEIGHT-10

        self.maxv = int(self.SCREEN_WIDTH*self.SCALE_WIDTH)
        self.accelaration = 2
        self.life_max = 5
        self.life = self.life_max
        self.now = pygame.time.get_ticks()
        self.last_powerup = 0
        self.bullets = 50
        self.gun_top = (
            int(self.rect.x+self.rect.w/2), 
            int(self.rect.top)
            )
        self.speedx = 0
        self.speedy = 0 
        self.shoot_speed  = -int(self.SCREEN_HEIGHT*self.SCALE_LENGTH*2.0)
        self.shoot_speedx = 0
        self.shoot_speedy = self.shoot_speed

#-------------------------------------------------------------------------------

    def update(self):
        self.now = pygame.time.get_ticks()
        self.move()

#-------------------------------------------------------------------------------

    def move(self):
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy  

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:

            if self.direction !='left':
                self.direction = 'left'
                self.image = self.image_left
                self.image.set_colorkey(self.BLACK)
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center  = center 
                self.bullet_img = self.bullet_img_left
                self.shoot_speedx = self.shoot_speed
                self.shoot_speedy = 0
            else:
                if self.speedx**2 < self.maxv**2:
                    self.speedx = self.speedx - int(self.accelaration/2.0)
                    # self.speedy = 0
                # self.rect.x += self.speedx


        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:

            if self.direction !='right':
                self.direction = 'right'
                self.image = self.image_right
                self.image.set_colorkey(self.BLACK)
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center  = center 
                self.bullet_img = self.bullet_img_right 
                self.shoot_speedx = -self.shoot_speed
                self.shoot_speedy = 0
            else:
                if self.speedx**2 < self.maxv**2:
                    self.speedx = self.speedx + int(self.accelaration/2.0)
                    # self.speedy = 0
                # self.rect.x += self.speedx

        if ((keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and
        (keystate[pygame.K_RIGHT] or keystate[pygame.K_d])):
            self.speedx = 0
            self.rect.x += self.speedx + self.speedx


        if self.rect.left   < self.X_BUFFER:
            self.rect.left  = self.X_BUFFER
            self.speedx = 0
        if self.rect.right  > self.SCREEN_WIDTH - self.X_BUFFER:
            self.rect.right = self.SCREEN_WIDTH - self.X_BUFFER
            self.speedx = 0


        if keystate[pygame.K_UP]:

            if self.direction !='up':
                self.direction = 'up'
                self.image = self.image_up
                self.image.set_colorkey(self.BLACK)
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center  = center 
                self.bullet_img = self.bullet_img_top 
                self.shoot_speedx = 0
                self.shoot_speedy = self.shoot_speed
            else:    
                if self.speedy**2 < self.maxv**2: 
                    self.speedy = self.speedy - int(self.accelaration/2.0)
                    # self.speedx = 0
                #self.rect.y += self.speedy


        if keystate[pygame.K_DOWN]:

            if self.direction !='down':
                self.direction = 'down'
                self.image = self.image_down
                self.image.set_colorkey(self.BLACK) 
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center  = center 
                self.bullet_img = self.bullet_img_bottom
                self.shoot_speedx = 0
                self.shoot_speedy = -self.shoot_speed
            else:
                if self.speedy**2 < self.maxv**2:
                    self.speedy = self.speedy + int(self.accelaration/2.0)
                    # self.speedx = 0
                #self.rect.y += self.speedy

        if self.rect.top < self.Y_BUFFER:
            self.rect.top = self.Y_BUFFER
            self.speedy= 0
        if self.rect.bottom > self.SCREEN_HEIGHT - self.Y_BUFFER:
            self.rect.bottom = self.SCREEN_HEIGHT - self.Y_BUFFER
            self.speedy = 0

#-------------------------------------------------------------------------------

    def shoot(self):
        self.gun_top = (self.rect.centerx, self.rect.centery)
        bullet = Bullet(self.bullet_img, self.gun_top[0], self.gun_top[1],
             self.shoot_speedx, self.shoot_speedy,
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )
        return bullet

#-------------------------------------------------------------------------------

    def show_life(self, surf, percentage, color, x, y):
        if percentage < 0:
            percentage = 0
        bar_w = int(self.SCREEN_WIDTH/10.0)
        bar_l = int(self.SCREEN_HEIGHT/100.0)
        fill_amount = (percentage/100.0)*bar_w
        outlline_rect = pygame.Rect(x, y, bar_w, bar_l)
        fill_rect = pygame.Rect(x, y, fill_amount, bar_l)
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, (255,255,255), outlline_rect, int(bar_l/3.0))

#-------------------------------------------------------------------------------

    def show_score(self,surf, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        render_font = pygame.font.Font(font_name, size)
        render_text = render_font.render(text, True, (255,255,0))
        text_rect = render_text.get_rect()

        text_rect.x, text_rect.y = (x, y)
        surf.blit(render_text, text_rect)

#-------------------------------------------------------------------------------
