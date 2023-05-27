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
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8

        # Alien settings
        self.alien_render = False
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.normal_alien_speedup_scale = 1.15
        self.better_alien_speedup_scale = 1.20
        self.bullet_speedup_scale = 1.3
        self.ship_speedup_scale = 1.25

        # How quickly the aliens points scale.
        self.score_scale = 1.5

    def initialize_dynamic_settings(self, mode):
        """Initialize settings that change troughout the game."""
        if mode == 'easy':
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.normal_alien_speed = 1.0
            self.normal_alien_points = 50
        elif mode == 'normal':
            self.ship_speed = 2.0
            self.bullet_speed = 2.5
            self.normal_alien_speed = 1.5
            self.better_alien_speed = 2.0
            self.normal_alien_points = 50
            self.better_alien_points = 80
        elif mode == 'hard':
            self.ship_speed = 2.5
            self.bullet_speed = 3.0
            self.normal_alien_speed = 2.0
            self.better_alien_speed = 2.5
            self.normal_alien_points = 60
            self.better_alien_points = 90

        # fleet directions of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and aliens point values."""
        self.ship_speed *= self.ship_speedup_scale
        self.bullet_speed *= self.bullet_speedup_scale
        self.normal_alien_speed *= self.normal_alien_speedup_scale
        self.better_alien_speed *= self.better_alien_speedup_scale

        self.normal_alien_points = int(self.normal_alien_points * self.score_scale)
        self.better_alien_points = int(self.better_alien_points * self.score_scale)