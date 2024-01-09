import socket
import json
import pygame
import pygame_gui
from pygame import sprite
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_HEIGHT, BUTTON_SPACING

class GameState(BaseState):
    def __init__(self, ui_manager, player_name, volume_percent, server_address):
        self.player_name = player_name
        self.volume_percent = volume_percent
        self.server_address = server_address
        self.ui_manager = ui_manager
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

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
        button_y = panel_height // 2 - (BUTTON_HEIGHT + BUTTON_SPACING) // 2

        self.create_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 4 - 100, button_y, 200, BUTTON_HEIGHT),
            text="Create New Room",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="create_room_button",
        )

        self.enter_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 2 - 100, button_y, 200, BUTTON_HEIGHT),
            text="Enter a Room",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="enter_room_button",
        )

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width * 3 // 4 - 100, button_y, 200, BUTTON_HEIGHT),
            text="Exit",
            manager=self.ui_manager,
            container=self.game_panel,
            object_id="exit_button",
        )

    def update(self, dt):
        self.ui_manager.update(time_delta=dt)


    def render(self, screen):
        self.ui_manager.draw_ui(screen)

    def handle_create_room(self):
        try:
            self.client_socket.sendall(b"create_queue")
            response = self.client_socket.recv(1024).decode()
            response_data = json.loads(response)
            queue_id = response_data["queue_id"]

            # Handle successful queue creation (e.g., display a message or transition to a room state)
            if queue_id is not None:
                print(f"Created queue with ID: {queue_id}")

                command = f"join_queue {queue_id} {self.player_name}"
                self.client_socket.sendall(command.encode())
                response = self.client_socket.recv(1024).decode()
                response_data = json.loads(response)

            # Example: Transition to a room state
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"state":"RoomState", "queue_id":queue_id}))

        except Exception as e:
            print(f"Error creating queue: {e}")
            # Handle errors (e.g., display an error message)