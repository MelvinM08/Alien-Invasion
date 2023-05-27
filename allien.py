import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single allien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its initial position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Initialize all the aliens
        self.normal_alien = AlienImage("Part II//Alien Invasion//images//alien.bmp")

        self.image = self.normal_alien.image
        self.rect = self.normal_alien.rect

    def check_edges(self):
        """Return True if alien is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.normal_alien.rect.right >= screen_rect.right) or (
            self.normal_alien.rect.left <= 0)

    def update(self):
        """Move the aliens right or left."""
        # Normal alien position.
        self.normal_alien.x += self.settings.normal_alien_speed * self.settings.fleet_direction
        self.normal_alien.rect.x = self.normal_alien.x

class BetterAlien(Sprite):
    """A class to the better alien."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.better_alien = AlienImage("Part II//Alien Invasion//images//alien_2.bmp")

        self.image = self.better_alien.image
        self.rect = self.better_alien.rect

    def check_edges(self):
        """Return True if alien is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.better_alien.rect.right >= screen_rect.right) or (
                self.better_alien.rect.left <= 0)

    def update(self):
        """Move the aliens right or left"""
        # Better alien position.
        self.better_alien.x += self.settings.better_alien_speed * self.settings.fleet_direction
        self.better_alien.rect.x = self.better_alien.x

class AlienImage:
    """A class to represent the image and position of an alien."""

    def __init__(self, image_path):
        """Initialize the alien image and set its rect attribute."""
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.x = self.rect.width
        self.y = self.rect.height
        self.x = float(self.rect.x)