import sys
import pygame
import random
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import BG
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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
        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #Llamamos a las demas clases
        self.bg = BG()
        self.bg_group = pygame.sprite.Group()
        self.bg_group.add(self.bg)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        #Creamos las naves aliens
        self._create_fleet()
        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Iniciamos el hilo principal del juego"""
        while True:
        #refactorizamos y separamos las funcionalidades del programa en funciones separadas

            self._check_events()
            if self.stats.game_active:  
                self.ship.update()
                self._update_aliens()
                
                self._update_bullets()
            self._update_screen()



    def _check_events(self):
        """Revisamos si alguna interaccion sucede con el teclado"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            self._check_keyup_events(event)
            self._check_keydown_events(event)
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            
            self.settings.initialize_dynamic_settings()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.stats.game_active = True   
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            

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
        if self.stats.game_active == True:
            if len(self.bullets) < self.settings.bullets_allowed:

                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

        
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
        number_rows = available_space_y // (3 * alien_height)
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

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()

        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:   
            # Decrement ship left, and update scoreboard.
            self.sb.prep_ships()
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active =False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
            
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        #Redibujar la pantalla por cada pasada
        
        
        self.bg_group.update()
        self.screen.fill(self.settings.bg_color)
        self.bg_group.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()
        
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        self.clock.tick(60)
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()