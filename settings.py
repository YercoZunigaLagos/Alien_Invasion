import pygame

class Settings:
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.display_size = (self.screen_width,self.screen_height)
        self.bg_color = (0,0,0)
        self.num_stars = 100
        # Colores
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        # Ship settings
        self.ship_speed = 5
        # Bullet settings
        self.bullet_speed = 5
        self.bullet_width = 7
        self.bullet_height = 20
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 5
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1    
        self.ship_limit = 3
        # How quickly the alien point values increase
        self.score_scale = 1.5
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1      
        # Scoring
        self.alien_points = 50  
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale      
        self.alien_points = int(self.alien_points * self.score_scale)