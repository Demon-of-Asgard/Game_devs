import pygame
import numpy
from bullets.bullets import Bullet

#-------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img,bullet_img, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.SCALE_WIDTH  = 1.0/35.0
        self.SCALE_LENGTH = 1.0/17.0
        self.Y_BUFFER  = 10
        self.X_BUFFER  = 5
        self.BLACK = (0, 0, 0)
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.bullet_img = bullet_img

        self.scale = (
            int(self.SCREEN_WIDTH*self.SCALE_WIDTH),
            int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
        )

        self.image_orig = pygame.transform.scale(player_img, self.scale)
        self.image  = self.image_orig.copy()
        self.rect   = self.image.get_rect()

        self.radius = int(
            (1.0/4.0)*numpy.sqrt(self.scale[0]**2+self.scale[1]**2)
        )

        self.image.set_colorkey(self.BLACK)
        self.rect.centerx = int(self.SCREEN_WIDTH/2)
        self.rect.bottom  = self.SCREEN_HEIGHT-10

        self.life_max = 5
        self.life = self.life_max
        self.speedx = 0
        self.speedy = 0
        self.rot = 0
        self.rot_speed = 90
#-------------------------------------------------------------------------------

    def update(self):
        self.move()

#-------------------------------------------------------------------------------

    def move(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -int(self.SCREEN_WIDTH*self.SCALE_WIDTH)
            self.rect.x += self.speedx


        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = int(self.SCREEN_WIDTH*self.SCALE_WIDTH)
            self.rect.x += self.speedx

        if ((keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and
        (keystate[pygame.K_RIGHT] or keystate[pygame.K_d])):
            self.speedx = 0
            self.rect.x += self.speedx



        if self.rect.left   < self.X_BUFFER:
            self.rect.left  = self.X_BUFFER
        if self.rect.right  > self.SCREEN_WIDTH - self.X_BUFFER:
            self.rect.right = self.SCREEN_WIDTH - self.X_BUFFER

        self.speedy = 0

        if keystate[pygame.K_UP]:
            self.speedy = -int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
            self.rect.y += self.speedy


        if keystate[pygame.K_DOWN]:
            self.speedy = int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
            self.rect.y += self.speedy

        if self.rect.top < self.Y_BUFFER:
            self.rect.top = self.Y_BUFFER
        if self.rect.bottom > self.SCREEN_HEIGHT - self.Y_BUFFER:
            self.rect.bottom = self.SCREEN_HEIGHT - self.Y_BUFFER

#-------------------------------------------------------------------------------

    def shoot_L(self):
        bullet = Bullet(
            self.bullet_img, self.rect.x, self.rect.top,
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )
        return bullet

#-------------------------------------------------------------------------------

    def shoot_R(self):
        bullet = Bullet(
            self.bullet_img, self.rect.x+self.rect.w, self.rect.top,
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

#--------------------------------------------------------------------------------

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
