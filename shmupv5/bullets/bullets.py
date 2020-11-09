import pygame
#-------------------------------------------------------------------------------

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, x, y, speedx, speedy, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.SCALE_WIDTH   = 1.0/200.0
        self.SCALE_LENGTH  = 1.0/25.0
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.BLACK = (0,0,0)

        self.image_orig = bullet_img
           
        self.image = self.image_orig.copy()
        self.image.set_colorkey(self.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = speedy    
        self.speedx = speedx 

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if (self.rect.bottom < 0 or self.rect.left > self.SCREEN_WIDTH or
            self.rect.top > self.SCREEN_HEIGHT or self.rect.right < 0
            ):
            self.kill()

#-------------------------------------------------------------------------------
