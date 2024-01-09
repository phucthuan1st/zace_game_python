import pygame_gui
import pygame
from .base_state import BaseState
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SERVER_ADDRESS

class SettingsState(BaseState):
    def __init__(self, ui_manager, player_name):
        super().__init__()
        self.ui_manager = ui_manager

        # Load settings from storage (replace with your loading logic)
        self.sound_setting = 50  # Load initial sound setting (50%)
        self.server_address = SERVER_ADDRESS  # Load initial server address
        self.player_name = player_name

        # Create UIPanel centered and sized as half of the screen
        panel_width = SCREEN_WIDTH // 2
        panel_height = SCREEN_HEIGHT // 2
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        self.settings_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.ui_manager,
            visible=False,
            object_id="settings_panel",
        )

        # Create UI elements within the panel
        self.sound_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, panel_width - 40, 25),
            text="Sound:",
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="sound_label",
        )
        self.sound_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(10, 40, panel_width - 20, 50),
            start_value=self.sound_setting,
            value_range=(0, 100),
            click_increment=10,
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="sound_slider",
        )
        self.server_address_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 100, panel_width - 40, 25),
            text="Server Address:",
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="server_address_label",
        )
        self.server_address_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 130, panel_width - 20, 30),
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="server_address_input",
        )

        (host, port) = self.server_address
        self.server_address_input.set_text(f"{host}:{port}")

        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 170, panel_width - 40, 25),
            text="Player Name:",
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="name_label",
        )
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 200, panel_width - 20, 30),
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="name_input",
        )
        self.name_input.set_text(self.player_name)

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, panel_height - 110, panel_width - 30, 40),
            text="Save",
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="save_settings_button",
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, panel_height - 60, panel_width - 30, 40),
            text="Exit",
            manager=self.ui_manager,
            container=self.settings_panel,
            object_id="exit_settings_button",
        )


    def update(self, dt):
        self.ui_manager.update(time_delta=dt)

        self.sound_setting = self.sound_slider.get_current_value()
        self.player_name = self.name_input.get_text()

        # Assuming self.server_address_input.get_text() contains a string in the format "host:port"
        address_str = self.server_address_input.get_text()

        # Split the string into host and port
        host, port = address_str.split(':')

        # Convert the port to an integer
        port = int(port)

        # Create the AF_INET address tuple
        server_address = (host, port)

        # Now, server_address is a valid AF_INET address tuple
        self.server_address = server_address



    def render(self, screen):
        self.ui_manager.draw_ui(screen)