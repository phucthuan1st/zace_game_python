import pygame
import pygame_gui
from pygame import sprite
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameState(BaseState):
    def __init__(self, ui_manager, play_name, volume_percent, server_address):
        self.play_name = play_name
        self.volume_percent = volume_percent
        self.server_address = server_address
        self.ui_manager = ui_manager

        # Create UIPanel covering the entire screen
        panel_width = SCREEN_WIDTH
        panel_height = SCREEN_HEIGHT
        self.game_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(0, 0, panel_width, panel_height),
            manager=self.ui_manager,
            visible=False,
            object_id="game_panel",
        )

        # Create buttons within the panel
        button_height = 50
        button_spacing = 20
        button_y = panel_height // 2 - (button_height + button_spacing) // 2

        self.create_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 4 - 100, button_y, 200, button_height),
            text="Create New Room",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="create_room_button",
        )

        self.enter_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 2 - 100, button_y, 200, button_height),
            text="Enter a Room",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="enter_room_button",
        )

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width * 3 // 4 - 100, button_y, 200, button_height),
            text="Exit",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="exit_button",
        )

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)


    def render(self, screen):
        self.ui_manager.draw_ui(screen)