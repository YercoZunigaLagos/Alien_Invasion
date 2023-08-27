import sys
import pygame
import random
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        #hagamos un cambio del color del background
        self.settings = Settings()
        #HACER EL JUEGO FULL PANTALLA
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        

        self.ship = Ship(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
        # Watch for keyboard and mouse events.
            self._check_events()
            self._update_screen()
     
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            self._check_keyup_events(event)
            self._check_keydown_events(event)

    def _check_keyup_events(self,event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
    def _check_keydown_events(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
    def _update_screen(self):
    #Redibujar la pantalla por cada pasada

        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        self.ship.update()
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        self.clock.tick(60)
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()