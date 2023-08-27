import pygame

class Settings:
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)
        self.num_stars = 100
        # Colores
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        # Ship settings
        self.ship_speed = 5
        