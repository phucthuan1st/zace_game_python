import pygame
import pygame_gui
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BaseState:
    def __init__(self):
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.ui_manager.process_events(event)

    def update(self, dt):
        self.ui_manager.update(dt)

    def render(self, screen):
        self.ui_manager.draw_ui(screen)
