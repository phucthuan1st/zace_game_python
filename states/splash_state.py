import pygame
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class SplashState(BaseState):
    def __init__(self):
        super().__init__()
        self.timer = 0

        unscaled_logo = pygame.image.load("assets/zacetankbattle-logo-transparent.png")
        scaling_factor = 0.2  # Adjust as needed
        self.logo_image = pygame.transform.scale(
            unscaled_logo, (int(unscaled_logo.get_width() * scaling_factor), int(unscaled_logo.get_height() * scaling_factor))
        )

    def update(self, dt):
        self.timer += dt
        if self.timer >= 2.0:  # Switch to MainMenuState after 1.5 seconds
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"state":"MainMenuState"}))

    def render(self, screen):
        screen.fill((0, 0, 0))  # Black background

        # Center the scaled logo on the screen
        screen.blit(self.logo_image, (
            (SCREEN_WIDTH - self.logo_image.get_width()) // 2,  # Center horizontally
            (SCREEN_HEIGHT - self.logo_image.get_height()) // 2  # Center vertically
        ))
