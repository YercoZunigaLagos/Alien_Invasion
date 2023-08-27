import pygame
from pygame.sprite import Sprite
import random

from settings import Settings

class Star(Sprite):
    def __init__(self):
        super(Star,self).__init__()
        self.settings = Settings()
        self.width = random.randrange(1,4)
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, self.settings.screen_width)
        self.vel_x = 0
        self.vel_y = random.randrange(4,25)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y