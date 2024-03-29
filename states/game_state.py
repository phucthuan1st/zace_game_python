import pygame
import pygame_gui
import json
import hashlib


from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_HEIGHT, BUTTON_SPACING, SERVER_ADDRESS, CELL_SIZE
from assets.Spritesheet import SpriteSheet

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

        self.tank_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.map_group = pygame.sprite.Group()

        # Create a gRPC channel and stub
        host, port = SERVER_ADDRESS
        self.channel = grpc.insecure_channel(f'{host}:{port}')  # Adjust server address if needed
        self.stub = zace_tank_battle_pb2_grpc.TankBattleServiceStub(self.channel)

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

        NUMBER_OF_CELL = SCREEN_HEIGHT // CELL_SIZE

        score_board_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                CELL_SIZE * NUMBER_OF_CELL, 
                BUTTON_HEIGHT, 
                SCREEN_WIDTH - CELL_SIZE * NUMBER_OF_CELL, 
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

        self.map_group.add(map_grid_sprite)

        join_request = zace_tank_battle_pb2.PlayerJoinRequest(player_name=self.player_name)
        self.game_stream = self.stub.JoinGame(join_request)

        self.spriteSheet = SpriteSheet("assets/gdm-top-down-sci-fi-tanks/Tanks.png")

        # Load sprite_sheet.json
        with open("assets/gdm-top-down-sci-fi-tanks/sprite_sheet.json", "r") as json_file:
            self.sprite_sheet_data = json.load(json_file)

        self.key_mapping = {
            pygame.K_w: "up",
            pygame.K_a: "left",
            pygame.K_s: "down",
            pygame.K_d: "right",
            pygame.K_SPACE: "shoot",
        }

        self.tank_direction = "up"

    def process_match_state(self, match_state):
        # Get the rect for the 'tier1_prototype' sprite
        tank_sprite_data = self.sprite_sheet_data["tier3_prototype"]
        bullet_sprite_data = self.sprite_sheet_data["tier2_missile"]

        # Create a surface with the specified rect from the sprite sheet
        tank_surface = self.spriteSheet.get_sprite(
            tank_sprite_data["rect"]["x"], 
            tank_sprite_data["rect"]["y"],
            tank_sprite_data["rect"]["width"], 
            tank_sprite_data["rect"]["height"]
        )

        bullet_surface = self.spriteSheet.get_sprite(
            bullet_sprite_data["rect"]["x"], 
            bullet_sprite_data["rect"]["y"],
            bullet_sprite_data["rect"]["width"], 
            bullet_sprite_data["rect"]["height"]
        )

        # Process the received game state
        for tank in match_state.tanks:

            # Resize the tank sprite if needed
            tank_surface = pygame.transform.scale(tank_surface, (CELL_SIZE, CELL_SIZE))

            # Determine the initial rotation based on tank's direction
            initial_rotation = 0
            if tank.direction == "left":
                initial_rotation = 90
            elif tank.direction == "down":
                initial_rotation = 180
            elif tank.direction == "right":
                initial_rotation = 270

            # Display the tank sprite on the screen
            self.tank_group.add(TankSprite(tank_surface, tank.position.x, tank.position.y, initial_rotation))

        # Process bullets
        for bullet in match_state.bullets:

            # Determine the initial rotation based on tank's direction
            initial_rotation = 0
            if bullet.direction == "left":
                initial_rotation = 90
            elif bullet.direction == "down":
                initial_rotation = 180
            elif bullet.direction == "right":
                initial_rotation = 270

            # Resize the tank sprite if needed
            bullet_surface = pygame.transform.scale(bullet_surface, (CELL_SIZE // 3, CELL_SIZE))

            # Display the bullet sprite on the screen
            self.bullet_group.add(BulletSprite(bullet_surface, bullet.position.x, bullet.position.y, initial_rotation))

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)
        self.map_group.update(time_delta=dt)

        self.tank_group.empty()
        self.bullet_group.empty()
    
        try:
            # Get the initial game state after joining
            self.match_state = next(self.game_stream)
            self.process_match_state(self.match_state)

            # Update sprite groups
            self.bullet_group.update(time_delta=dt)
            self.tank_group.update(time_delta=dt)
        except grpc.RpcError as e:
            print(f"Error during game streaming: {e}")

    def render(self, screen):
        self.ui_manager.draw_ui(screen)
        self.map_group.draw(screen)
        self.bullet_group.draw(screen)
        self.tank_group.draw(screen)

    def handle_keypress(self, key):
        if key != pygame.K_SPACE:

            try:
                direction = self.key_mapping[key]
            except KeyError:
                return

            # Generate player_id as SHA-256 hash of player_name
            player_name_bytes = self.player_name.encode('utf-8')
            player_id = hashlib.sha256(player_name_bytes).hexdigest()
            # Send the move action to the server
            move_action = zace_tank_battle_pb2.PlayerAction(
                player_id=player_id,
                action_type="move",
                direction=direction
            )

            self.tank_direction = direction
            self.stub.SendAction(move_action)
        elif key == pygame.K_SPACE:
            # Generate player_id as SHA-256 hash of player_name
            player_name_bytes = self.player_name.encode('utf-8')
            player_id = hashlib.sha256(player_name_bytes).hexdigest()
            
            # Send the shoot action to the server
            shoot_action = zace_tank_battle_pb2.PlayerAction(
                player_id=player_id,
                action_type="shoot",
                direction=self.tank_direction
            )
            self.stub.SendAction(shoot_action)
