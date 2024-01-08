import pygame
import pygame_gui
from states.splash_state import SplashState
from states.main_menu_state import MainMenuState 
from states.settings_state import SettingsState;
# from states.game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class StateManager:
    def __init__(self, ui_manager):
        self.states = {
            "SplashState": SplashState(),
            "MainMenuState": MainMenuState(ui_manager),
            "SettingsState": SettingsState(ui_manager),
            #"GameState": GameState(),
        }

        self.current_state = self.states.get("SplashState")

    def change_state(self, new_state):
        self.current_state = self.states.get(new_state)

    def update(self, dt):
        self.current_state.update(dt)

    def render(self, screen):
        self.current_state.render(screen)

def main():
    pygame.init()
    pygame.display.set_caption("Zace Tank Battle")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    state_manager = StateManager(ui_manager)

    running = True
    while running:
        for event in pygame.event.get():
            # pygame_gui button event handlers
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # PLAY button event
                if event.ui_object_id == "play_button":
                    state_manager.change_state(GameState())
               
                # SETTINGS button events
                elif event.ui_object_id == "settings_button":
                    state_manager.change_state("SettingsState")
                    state_manager.current_state.is_active = True

                elif event.ui_object_id == "save_settings_button":
                    state_manager.change_state("MainMenuState")

                elif event.ui_object_id == "exit_settings_button":
                    state_manager.change_state("MainMenuState")

                # QUIT button event
                elif event.ui_object_id == "quit_button":
                    running = False

            # user defined event handlers
            elif event.type == pygame.USEREVENT:
                new_state = event.dict.get('state')
                if new_state is not None:
                    state_manager.change_state(new_state)

            # QUIT event handler
            elif event.type == pygame.QUIT:
                running = False

            ui_manager.process_events(event=event)

        state_manager.update(float(clock.tick(FPS) / 1000))
        state_manager.render(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
