import pygame
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame_gui.elements import UIButton

class MainMenuState(BaseState):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager

# Load and scale logo
        unscaled_logo = pygame.image.load("assets/zacetankbattle-logo-transparent.png")
        scaling_factor = 0.15  # Adjust as needed
        self.logo_image = pygame.transform.scale(
            unscaled_logo, (int(unscaled_logo.get_width() * scaling_factor), int(unscaled_logo.get_height() * scaling_factor))
        )

        # Calculate button dimensions and spacing
        button_width = int(SCREEN_WIDTH * 0.25)  # 20% of screen width
        button_height = int(SCREEN_HEIGHT * 0.05)  # 5% of screen height
        button_spacing = int(SCREEN_HEIGHT * 0.03)  # 2% of screen height

        # Calculate button positions based on logo and spacing
        logo_bottom = (SCREEN_HEIGHT // 4) + self.logo_image.get_height() // 2 + (button_height // 2)
        button_y_start = logo_bottom + button_spacing
        button_y_increment = button_height + button_spacing

        # Create buttons
        self.play_button = UIButton(
            pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 
                        button_y_start,
                        button_width, button_height),
            "Play",
            self.ui_manager,
            object_id="play_button"
        )
        self.settings_button = UIButton(
            pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                        button_y_start + button_y_increment,
                        button_width, button_height),
            "Settings",
            self.ui_manager,
            object_id="settings_button"
        )
        self.quit_button = UIButton(
            pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                        button_y_start + button_y_increment * 2,
                        button_width, button_height),
            "Quit",
            self.ui_manager,
            object_id="quit_button"
        )

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)

    def render(self, screen):
        screen.fill((200, 200, 200))  # Light gray background
        screen.blit(self.logo_image, (SCREEN_WIDTH // 2 - self.logo_image.get_width() // 2,
                                      SCREEN_HEIGHT // 4 - self.logo_image.get_height() // 2))

        # Draw UI elements (including buttons)
        self.ui_manager.draw_ui(screen)
