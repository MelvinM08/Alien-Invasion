import sys
import pygame
from time import sleep
from random import randint

from settings import Settings
from ship import Ship
from bullets import Bullet
from allien import Alien
from allien import BetterAlien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                              self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statics.
        self.stats = GameStats(self)

        # Create a scoreboard instance.
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.normal_aliens = pygame.sprite.Group()
        self.better_aliens = pygame.sprite.Group()

        # Set the background color.
        self.bg_color = (230, 230, 230)

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play buttons.
        self.play_buttons = Button(self, "Easy Mode", "Normal Mode", "Hard Mode")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_buttons(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()


    def _check_keyup_events(self, event):
        """Respond to releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_buttons(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        easy_button_clicked = self.play_buttons.easy_button_rect.collidepoint(mouse_pos)
        normal_button_clicked = self.play_buttons.normal_button_rect.collidepoint(mouse_pos)
        hard_button_clicked = self.play_buttons.hard_button_rect.collidepoint(mouse_pos)

        if not self.game_active:
            if easy_button_clicked:
                self.actual_mode = 'easy'
                self._start_game(self.actual_mode)
            elif normal_button_clicked:
                self.actual_mode = 'normal'
                self._start_game(self.actual_mode)
            elif hard_button_clicked:
                self.actual_mode = 'hard'
                self._start_game(self.actual_mode)

    def _start_game(self, difficult):
        """Just start the game if its inactive."""
        if not self.game_active:
            # Reset the game stats.
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.game_active = True
        
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.normal_aliens.empty()
            self.better_aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Show the aliens
            self.settings.alien_render = True

            # Reset the game settings.
            self.settings.initialize_dynamic_settings(difficult)

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _fire_bullets(self):
        """Create a new bullet and add it to the bullets group."""
        if self.game_active:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet) 

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Get ride of bullets that have dissapeard.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision."""
        # Remove any bullets and aliens that have collided.
        normal_alien_collide = pygame.sprite.groupcollide(self.bullets, self.normal_aliens,
                                                True, True)
        better_alien_collide = pygame.sprite.groupcollide(self.bullets, self.better_aliens,
                                                            True, True)
        
        if normal_alien_collide:
            for aliens in normal_alien_collide.values():
                self.stats.score += self.settings.normal_alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if better_alien_collide:
            for aliens in better_alien_collide.values():
                self.stats.score += self.settings.better_alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        
        if not self.normal_aliens and not self.better_aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """Update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.normal_aliens.update()
        if self.actual_mode == 'normal' or self.actual_mode == 'hard':
            self.better_aliens.update()

        self._check_alien_ship_collisions()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_alien_ship_collisions(self):
        """Respond to alien-ship collision."""
        if pygame.sprite.spritecollideany(self.ship, self.normal_aliens):
            self._ship_hit()
        if pygame.sprite.spritecollideany(self.ship, self.better_aliens):
            self._ship_hit()

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.normal_alien.rect.size

        current_x, current_y = alien_width, alien_height
        row_size = 0
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width -2 * alien_width):
                if self.actual_mode == 'easy':
                    alien_type = 1
                    self._create_alien(current_x, current_y, alien_type)
                    current_x += 2 * alien_width
                elif self.actual_mode == 'normal':
                    if row_size == 0 or row_size == 4:
                        alien_type = 1
                        self._create_alien(current_x, current_y, alien_type)
                        current_x += 2 * alien_width
                        row_size += 1
                    else:
                        alien_type = randint(1, 2)
                        self._create_alien(current_x, current_y, alien_type)
                        current_x += 2 * alien_width
                        row_size += 1
                elif self.actual_mode == 'hard':
                    if row_size == 0 or row_size == 4:
                        alien_type = 2
                        self._create_alien(current_x, current_y, alien_type)
                        current_x += 2 * alien_width
                        row_size += 1
                    else:
                        alien_type = randint(1, 2)
                        self._create_alien(current_x, current_y, alien_type)
                        current_x += 2 * alien_width
                        row_size += 1

            # Finished a row; reset x value and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
            row_size = 0
            

    def _create_alien(self, x_position, y_position, alien_type):
        """Create an alien and place it in the row."""
        if alien_type == 1:
            new_alien = Alien(self)
            new_alien.normal_alien.x = x_position
            new_alien.normal_alien.rect.x = x_position
            new_alien.normal_alien.rect.y = y_position
            self.normal_aliens.add(new_alien)
        elif alien_type == 2:
            new_alien = BetterAlien(self)
            new_alien.better_alien.x = x_position
            new_alien.better_alien.rect.x = x_position
            new_alien.better_alien.rect.y = y_position
            self.better_aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for normal_alien in self.normal_aliens.sprites():
            if normal_alien.check_edges():
                self._change_fleet_direction()
                break
        for better_alien in self.better_aliens.sprites():
            if better_alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if an alien have reached the bottom of the screen."""
        for normal_alien in self.normal_aliens.sprites():
            if normal_alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        for better_alien in self.better_aliens.sprites():
            if better_alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for normal_alien in self.normal_aliens.sprites():
            normal_alien.rect.y += self.settings.fleet_drop_speed

        for better_alien in self.better_aliens.sprites():
            better_alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """Respond to ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.normal_aliens.empty()
            self.better_aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Restart dynamic settings.
            self.settings.initialize_dynamic_settings(self.actual_mode)

            # Pause.
            sleep(0.6)
        else:
            self.game_active = False
            self.settings.alien_render = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        if self.settings.alien_render:
            self.normal_aliens.draw(self.screen)
            if self.actual_mode == 'normal' or self.actual_mode == 'hard':
                self.better_aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_buttons.draw_buttons()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()