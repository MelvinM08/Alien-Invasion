import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, *msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Common settings.
        self.buttons_width, self.buttons_height = 200, 50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('modernno20', 34)

        # Set the properties of the buttons.
        self._set_buttons_properties()

        # The button message need to be prepped only once.
        self._prep_msg(msg)

    def _set_buttons_properties(self):
        """Initialize all the button's properties."""
        # Easy mode button
        self.easy_button_color = (0, 0, 135)
        self.easy_button_rect = pygame.Rect(300, 150, self.buttons_width, self.buttons_height)

        # Normal mode button
        self.normal_button_color = (0, 135, 0)
        self.normal_button_rect = pygame.Rect(0, 0, self.buttons_width, self.buttons_height)
        self.normal_button_rect.center = self.screen_rect.center

        # Hard mode button
        self.hard_button_color = (135, 0, 0)
        self.hard_button_rect = pygame.Rect(300, 400, self.buttons_width, self.buttons_height)
    
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the buttons"""
        # Easy mode button
        self.easy_msg_image = self.font.render(msg[0], True, self.text_color,
                                          self.easy_button_color)
        self.easy_msg_image_rect = self.easy_msg_image.get_rect()
        self.easy_msg_image_rect.center = self.easy_button_rect.center

        # Normal mode button
        self.normal_msg_image = self.font.render(msg[1], True, self.text_color,
                                          self.normal_button_color)
        self.normal_msg_image_rect = self.normal_msg_image.get_rect()
        self.normal_msg_image_rect.center = self.normal_button_rect.center

        # Hard mode button
        self.hard_msg_image = self.font.render(msg[2], True, self.text_color,
                                          self.hard_button_color)
        self.hard_msg_image_rect = self.hard_msg_image.get_rect()
        self.hard_msg_image_rect.center = self.hard_button_rect.center

    def draw_buttons(self):
        """Draw blank buttons and then draw their message."""
        # Easy button
        self.screen.fill(self.easy_button_color, self.easy_button_rect)
        self.screen.blit(self.easy_msg_image, self.easy_msg_image_rect)

        # Normal button
        self.screen.fill(self.normal_button_color, self.normal_button_rect)
        self.screen.blit(self.normal_msg_image, self.normal_msg_image_rect)

        # Hard button
        self.screen.fill(self.hard_button_color, self.hard_button_rect)
        self.screen.blit(self.hard_msg_image, self.hard_msg_image_rect)