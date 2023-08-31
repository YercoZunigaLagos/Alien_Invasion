import pygame

class Ship:

    def __init__(self,ai_game):
        self.screen = ai_game.screen
        
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #cargar la imagen i colocarla recta
        self.image = pygame.transform.scale(pygame.image.load('images\ship_izquierda.png'), (50, 50))
        

        self.rect = self.image.get_rect()
        
        #Iniciar cada nueva nave en el centro abajo de la imagen
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.rotation = False 

    def update(self):
        """Update the ship's position based on the movement flag."""

         
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  
        # Update rect object from self.x.
       
        self.rect.x = self.x
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):

        """Dibujar la nave en su posicion actual"""
        self.screen.blit(self.image, self.rect,)