import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_anim, size):
        pygame.sprite.Sprite.__init__(self)
        self.size  = size 
        self.explosion_anim = explosion_anim
        self.image = explosion_anim[self.size][0]
        self.rect  = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0 
        self.last_updated = pygame.time.get_ticks()
        self.delay = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.delay:
            self.last_updated = now 
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center 
                self.image  = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 
