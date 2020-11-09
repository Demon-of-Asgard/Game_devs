import pygame
import numpy
import math
import random
#-------------------------------------------------------------------------------

class Mob(pygame.sprite.Sprite):
    def __init__(self, enemy_img, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.SPEED_SCALEX = 1.0/150.0
        self.SPEED_SCALEY = 1.0/100.0
        self.SCALE_WIDTH   = 1.0/25.0
        self.SCALE_LENGTH  = 1.0/12.0
        self.BLACK = (0, 0, 0)

        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.scale = (
        int(self.SCREEN_WIDTH*self.SCALE_WIDTH),
        int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
        )
        self.speedy = (
        random.randrange(int(self.SCREEN_HEIGHT*self.SPEED_SCALEY/2.0),
        int(self.SCREEN_HEIGHT*self.SPEED_SCALEY))
        )
        self.speedx = (
        random.randrange(-int(self.SCREEN_WIDTH*self.SPEED_SCALEX),
        int(self.SCREEN_WIDTH*self.SPEED_SCALEX))
        )

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
        self.image.set_colorkey(self.BLACK)
        self.rect.x = random.randint(0, self.SCREEN_WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if (
        self.rect.top > self.SCREEN_HEIGHT + 10 or self.rect.left < -25 or
        self.rect.right > self.SCREEN_WIDTH + 25
        ):
            self.speedy = (
            random.randrange(int(self.SCREEN_HEIGHT*self.SPEED_SCALEY/2.0),
            int(self.SCREEN_HEIGHT*self.SPEED_SCALEY))
            )
            self.speedx = (
            random.randrange(-int(self.SCREEN_WIDTH*self.SPEED_SCALEX),
            int(self.SCREEN_WIDTH*self.SPEED_SCALEX))
            )

            self.speedr = math.sqrt(self.speedx**2+self.speedy**2)

            if self.speedx <= 0:
                self.head = -int(
                math.acos(self.speedy/self.speedr)*(180.0/math.pi)
                )
            if self.speedx > 0:
                self.head = int(
                math.acos(self.speedy/self.speedr)*(180.0/math.pi)
                )
            new_image = pygame.transform.rotate(self.image_orig, self.head)

            self.image = new_image
            self.rect  = self.image.get_rect()
            self.image.set_colorkey(self.BLACK)

            self.rect.x = random.randint(0, self.SCREEN_WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100, -40)

#-------------------------------------------------------------------------------
