import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single allien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its initial position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("Part II//Alien Invasion//images//allien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.x = self.rect.width
        self.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x