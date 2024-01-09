import pygame
import pygame_gui
from states.splash_state import SplashState
from states.main_menu_state import MainMenuState 
from states.settings_state import SettingsState;
from helpers.random_name_generator import generate_random_name
from states.game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class StateManager:
    def __init__(self, ui_manager, player_name):
        self.states = {
            "SplashState": SplashState(),
            "MainMenuState": MainMenuState(ui_manager),
            "SettingsState": SettingsState(ui_manager, player_name),
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

    volume_percent = 50
    server_address = ""
    player_name = generate_random_name()

    state_manager = StateManager(ui_manager, player_name)

    # Initialize Pygame mixer for sound
    pygame.mixer.init()
    soundtrack = pygame.mixer.Sound("assets/Soviet_March.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            ui_manager.process_events(event=event)

            # pygame_gui button event handlers
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # PLAY button event
                if event.ui_object_id == "play_button":
                    state_manager.states["GameState"] = GameState(ui_manager, player_name, volume_percent, server_address)
                    state_manager.change_state("GameState")
                    state_manager.current_state.game_panel.show()
               
                # SETTINGS button events
                elif event.ui_object_id == "settings_button":
                    state_manager.change_state("SettingsState")
                    state_manager.current_state.settings_panel.show()

                elif event.ui_object_id == "settings_panel.save_settings_button" or event.ui_object_id == "settings_panel.exit_settings_button":
                    # Access and modify the SettingsState instance
                    settings_state = state_manager.current_state  # Assuming current state is SettingsState
                    settings_state.settings_panel.hide()
                    
                    if event.ui_object_id == "settings_panel.save_settings_button":
                        # TODO: Save settings to storage
                        volume_percent = settings_state.sound_setting
                        server_address = settings_state.server_address

                        print(f'Update Sound to {volume_percent} and server address to {server_address}')

                        player_name = settings_state.player_name 
                        print(f'Update Player to {player_name}')
                    
                    state_manager.change_state("MainMenuState")
                elif event.ui_object_id == "game_panel.exit_button":

                    # cleanup
                    game_state = state_manager.current_state
                    game_state.game_panel.kill()
                    del game_state

                    # change back to main menu state
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

        # Set the soundtrack's volume based on volume_percent
        soundtrack.set_volume(volume_percent / 100)

        # Play the soundtrack in a loop (if not already playing)
        if not pygame.mixer.get_busy():
            soundtrack.play(-1)

        state_manager.update(float(clock.tick(FPS) / 1000))
        state_manager.render(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
