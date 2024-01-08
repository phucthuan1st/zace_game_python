import pygame
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class SplashState(BaseState):
    def __init__(self):
        super().__init__()
        self.logo_image = pygame.image.load("assets/zacetankbattle-logo-transparent.png")
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= 1.5:  # Switch to MainMenuState after 1.5 seconds
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"state":"MainMenuState"}))

    def render(self, screen):
        screen.fill((0, 0, 0))  # Black background

        # Scale the logo image to half screen size
        scaled_logo = pygame.transform.scale(self.logo_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Center the scaled logo on the screen
        screen.blit(scaled_logo, (
            (SCREEN_WIDTH - scaled_logo.get_width()) // 2,  # Center horizontally
            (SCREEN_HEIGHT - scaled_logo.get_height()) // 2  # Center vertically
        ))
