import pygame, random, numpy 

class Powerup(pygame.sprite.Sprite):
    def __init__(self, dict_image, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.SCALE_WIDTH   = 1.0/40.0
        self.SCALE_LENGTH  = 1.0/20.0
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.BLACK = (0,0,0)
        self.type = random.choice(['life', 'bullet'])
        self.speedx = 0
        self.speedy = 2

        if self.type == 'life':
            self.image = pygame.transform.scale(
                dict_image[self.type],
                (int(self.SCREEN_WIDTH*self.SCALE_WIDTH),
                int(self.SCREEN_WIDTH*self.SCALE_WIDTH))
            )
            self.image.set_colorkey(self.BLACK)

        if self.type == 'bullet':
            self.image = pygame.transform.scale(
                dict_image[self.type],
                (int(self.SCREEN_WIDTH*self.SCALE_WIDTH*2),
                int(self.SCREEN_WIDTH*self.SCALE_WIDTH*2))
            )
            self.image.set_colorkey(self.BLACK)

        self.rect = self.image.get_rect()
        self.scale = (
            int(self.SCREEN_WIDTH*self.SCALE_WIDTH),
            int(self.SCREEN_HEIGHT*self.SCALE_LENGTH)
        )

        self.radius = int(
            (1.0/4.0)*numpy.sqrt(self.scale[0]**2+self.scale[1]**2)
        )
        self.rect.centerx = random.randrange(0, self.SCREEN_WIDTH)
        self.rect.centery = random.randrange(-40, -10)

    def update(self):
        self.rect.centery += self.speedy
        if self.rect.top > self.SCREEN_HEIGHT:
            self.kill()