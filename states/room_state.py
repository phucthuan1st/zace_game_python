import socket
import json
import pygame
import pygame_gui
from pygame import sprite
from .base_state import BaseState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_HEIGHT, BUTTON_SPACING

class RoomState(BaseState):
    def __init__(self, ui_manager, client_socket, queue_id):
        super().__init__()
        self.client_socket = client_socket
        self.queue_id = queue_id
        self.user_list = []
        self.ui_manager = ui_manager

        # Create UI elements
        panel_width = SCREEN_WIDTH
        panel_height = SCREEN_HEIGHT

        self.room_panel = pygame_gui.elements.UIPanel(
            # Adjust panel dimensions and positioning as needed
            relative_rect=pygame.Rect(0, 0, panel_width, panel_height),  # Example dimensions
            manager=self.ui_manager,
            object_id="room_panel",
            visible=False
        )

        button_width = 150

        self.leave_room_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, BUTTON_HEIGHT // 2, button_width, BUTTON_HEIGHT),  # Adjust position
            text="Leave Room",
            manager=self.ui_manager,
            container=self.room_panel,
            object_id="leave_room_button",
        )

    def create_user_label(self, user_index, user_name, starting_y):
        id = f"user_label_{user_index}"

        label_width = 200  # Adjust as needed
        label_height = 30

        # Calculate centered horizontal position for label
        label_x = (SCREEN_WIDTH - label_width) // 2

        # Position label below the leave button with vertical spacing
        y_position = starting_y + BUTTON_HEIGHT + BUTTON_SPACING  # Adjust spacing as needed

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(label_x, y_position, label_width, label_height),
            text=user_name,
            manager=self.ui_manager,
            container=self.room_panel,
            object_id=id,
        )

    def update(self, dt):
        self.request_queue_info()
        self.ui_manager.update(time_delta=dt)

    def render(self, screen):
        self.ui_manager.draw_ui(screen)

    def request_queue_info(self):
        try:
            self.client_socket.sendall(b"get_queue_info " + self.queue_id.encode())
            response = self.client_socket.recv(1024).decode()
            data = json.loads(response)

            self.user_list = data.get("users", [])

            # Update UI labels based on the new user list
            current_y = 10
            for user_index, user in enumerate(self.user_list):
                self.create_user_label(user_index, user["name"], current_y)
                current_y += 30 + 20

        except socket.error as e:
            print("Error communicating with server:", e)
            # Handle errors (e.g., display an error message)

    def handle_leave_room(self):
        try:
            self.client_socket.sendall(b"leave_queue " + self.queue_id.encode())
            response = self.client_socket.recv(1024).decode()
            
            data = json.loads(response)
            message = data["message"]

            if message != "Left queue successfully":
                print("Left queue failed")
            else:
                print(message)

        except socket.error as e:
            print("Error communicating with server:", e)

        