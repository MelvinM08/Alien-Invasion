class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullets settings
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.alien_speedup_scale = 1.15
        self.bullet_speedup_scale = 1.3
        self.ship_speedup_scale = 1.25

    def initialize_dynamic_settings(self, mode):
        """Initialize settings that change troughout the game."""
        if mode == 'easy':
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif mode == 'normal':
            self.ship_speed = 2.0
            self.bullet_speed = 2.5
            self.alien_speed = 1.5
        elif mode == 'hard':
            self.ship_speed = 2.5
            self.bullet_speed = 2.5
            self.alien_speed = 2.0

        # fleet directions of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.ship_speedup_scale
        self.bullet_speed *= self.bullet_speedup_scale
        self.alien_speed *= self.alien_speedup_scale