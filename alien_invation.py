import sys
import pygame
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Clase Principal para manejar el juego"""
    def __init__(self):
        """Inicializar el juego con sus configuraciones """
        pygame.init()
        self.settings = Settings()
        #HACER EL JUEGO FULL PANTALLA
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        
        #Llamamos a las demas clases
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        #Creamos las naves aliens
        self._create_fleet()


    def run_game(self):
        """Iniciamos el hilo principal del juego"""
        while True:
        #refactorizamos y separamos las funcionalidades del programa en funciones separadas
            self._check_events()
            self.ship.update()
            self.bullets.update()

            self._update_screen()
            #Eliminar balas que desaparecen
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <=0:
                    self.bullets.remove(bullet)
            
    def _check_events(self):
        """Revisamos si alguna interaccion sucede con el teclado"""
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
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_q:
                sys.exit()
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:

            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        #agregar una nave
        alien = Alien(self)
        
        #tomar los tamaños de la naves (imagen) y estimar el espacio libre disponible
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)
        #Determinamos el numero de filas de aliens que entran en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)
        print(number_rows)
        #realizamos un ciclo el cual nos permita dibujar todas las naves
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                #creamos el alien y lo colocamos en la fila
                self._create_alien(alien_number, row_number)

            


    def _create_alien(self,alien_number, row_number):

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        
        self.aliens.add(alien)


    def _update_screen(self):
        #Redibujar la pantalla por cada pasada

        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        self.clock.tick(60)
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()