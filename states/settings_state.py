import pygame_gui
import pygame
from .base_state import BaseState
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class SettingsState(BaseState):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager

        # Load settings from storage (replace with your loading logic)
        self.sound_setting = 50  # Load initial sound setting (50%)
        self.server_address = "https://zacegame.nguyenphucthuan.id.vn"  # Load initial server address

        self.settings_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  
        self.is_active = False

        # Create UI elements
        self.sound_slider = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect(100, 100, 200, 50),
            start_value=self.sound_setting, # Set initial slider position
            value_range=(0, 100),
            click_increment=10,  # 10% increments
            manager=self.ui_manager,
            visible=self.is_active,
            object_id="sound_slider"
        )
        self.server_address_input = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(100, 200, 200, 30),
            manager=self.ui_manager,
            visible=self.is_active,
            object_id="server_address_input"
        )
        self.server_address_input.set_text(self.server_address)  # Set initial text

        # ... (add buttons for saving and exiting settings)
        # Create save and exit buttons
        self.save_button = pygame_gui.elements.UIButton(
            pygame.Rect(150, 300, 100, 40),
            text="Save",
            manager=self.ui_manager,
            visible=self.is_active,
            object_id="save_settings_button"
        )
        self.exit_button = pygame_gui.elements.UIButton(
            pygame.Rect(350, 300, 100, 40),
            text="Exit",
            manager=self.ui_manager,
            visible=self.is_active,
            object_id="exit_settings_button"
        )

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)

        # Update settings based on UI element values
        self.sound_setting = self.sound_slider.get_current_value()
        self.server_address = self.server_address_input.get_text()

        self.sound_slider._set_visible(self.is_active)
        self.server_address_input._set_visible(self.is_active)
        self.save_button._set_visible(self.is_active)
        self.exit_button._set_visible(self.is_active)

    def render(self, screen):
        self.settings_surface.fill((100, 100, 100))  # Background color
        self.ui_manager.draw_ui(self.settings_surface)

        screen.blit(self.settings_surface, (0,0))