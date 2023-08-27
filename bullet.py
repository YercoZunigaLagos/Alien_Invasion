import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #crear una bala recta en (0,0) y despues colocarla en su correcta posicion
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop =ai_game.ship.rect.midtop

        #guardar la posicion de la bala como valor decimal
        self.y = float(self.rect.y)
    
    def update(self):
        #actualizar la posicion decimal de la bala
        self.y -= self.settings.bullet_speed
        #actualizar la posicion recta de la bala
        self.rect.y = self.y

    def draw_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)