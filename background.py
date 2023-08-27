import pygame
from settings import Settings
from star import Star
from pygame.sprite import Sprite
import random

class BG(Sprite):
    def __init__(self):
        super(BG,self).__init__()
        self.settings = Settings()
        self.image = pygame.Surface(self.settings.display_size)
        self.color = (0,0,15)
        self.image.fill(self.color)
        self.rect =self.image.get_rect()

        self.stars = pygame.sprite.Group()
        self.timer = random.randrange(1,10)




    def update(self):
        self.stars.update()
        if self.timer == 0:
            new_star = Star()
            self.stars.add(new_star)
            self.timer = random.randrange(1,10)
        
        self.image.fill(self.color)
        self.stars.draw(self.image)
        self.timer -= 1
