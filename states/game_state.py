import pygame
import pygame_gui

from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_HEIGHT, BUTTON_SPACING, SERVER_ADDRESS, CELL_SIZE

import grpc
import zace_tank_battle_pb2
import zace_tank_battle_pb2_grpc

from assets.Sprites import *

class GameState(BaseState):
    def __init__(self, ui_manager, player_name, volume_percent, server_address):
        self.player_name = player_name
        self.volume_percent = volume_percent
        self.server_address = server_address
        self.ui_manager = ui_manager

        # Create a gRPC channel and stub
        host, port = SERVER_ADDRESS
        channel = grpc.insecure_channel(f'{host}:{port}')  # Adjust server address if needed
        self.stub = zace_tank_battle_pb2_grpc.TankBattleServiceStub(channel)

        # Create UIPanel covering the entire screen
        panel_width = SCREEN_WIDTH
        panel_height = SCREEN_HEIGHT
        self.game_panel = pygame_gui.elements.UIPanel(
            pygame.Rect(0, 0, panel_width, panel_height),
            manager=self.ui_manager,
            visible=False,
            object_id="game_panel",
        )

        BUTTON_WIDTH = 200

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
            text="Exit",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="exit_button",
        )

        score_board_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                CELL_SIZE * 24, 
                BUTTON_HEIGHT, 
                SCREEN_WIDTH - CELL_SIZE * 24, 
                SCREEN_HEIGHT - BUTTON_HEIGHT
            ),
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="score_board",
        )

        map_grid_response = self.stub.GetMapGrid(zace_tank_battle_pb2.Empty())

        map_grid = []
        for row in map_grid_response.rows:
            cells = row.cells

            map_row_cells = []
            for cell in cells:
                map_row_cells.append(cell)

            map_grid.append(map_row_cells)

        map_grid_sprite = MapGrid(map_grid)
        map_grid_sprite.create_map()  # Generate the map using the received map grid

        self.map_group = pygame.sprite.Group()
        self.map_group.add(map_grid_sprite)

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)
        self.map_group.update(time_delta=dt)

    def render(self, screen):
        self.ui_manager.draw_ui(screen)
        self.map_group.draw(screen)