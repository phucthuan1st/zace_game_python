import pygame
import pygame_gui

from states.game_state import GameState
from states.splash_state import SplashState
from states.settings_state import SettingsState
from states.main_menu_state import MainMenuState 

class StateManager:
    def __init__(self, ui_manager, player_name, volume_percent, server_address):
        self.states = {
            "SplashState": SplashState(),
            "MainMenuState": MainMenuState(ui_manager),
            "SettingsState": SettingsState(ui_manager, player_name),
        }

        self.current_state = self.states.get("SplashState")
        self.ui_manager = ui_manager
        self.player_name = player_name
        self.server_address = server_address
        self.volume_percent = volume_percent
        self.is_running = True

    def change_state(self, new_state):
        self.current_state = self.states.get(new_state)

    def update(self, dt):
        self.current_state.update(dt)

    def render(self, screen):
        self.current_state.render(screen)

    def handle_events(self, event):
        self.ui_manager.process_events(event=event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            self.handle_button_events(event)
        elif event.type == pygame.USEREVENT:
            new_state = event.dict.get('state')
            if new_state is not None:
                self.change_state(new_state)
        elif event.type == pygame.QUIT:
            self.is_running = False

    def handle_button_events(self, event):
        # PLAY button event
        if event.ui_object_id == "play_button":
            self.states["GameState"] = GameState(self.ui_manager, self.player_name, self.volume_percent, self.server_address)
            self.change_state("GameState")
            self.current_state.game_panel.show()
        
        # SETTINGS button events
        elif event.ui_object_id == "settings_button":
            self.change_state("SettingsState")
            self.current_state.settings_panel.show()

        elif event.ui_object_id == "settings_panel.save_settings_button" or event.ui_object_id == "settings_panel.exit_settings_button":
            # Access and modify the SettingsState instance
            settings_state = self.current_state  # Assuming current state is SettingsState
            settings_state.settings_panel.hide()
            
            if event.ui_object_id == "settings_panel.save_settings_button":
                # TODO: Save settings to storage
                self.volume_percent = settings_state.sound_setting
                self.server_address = settings_state.server_address

                print(f'Update Sound to {self.volume_percent} and server address to {self.server_address}')

                self.player_name = settings_state.player_name 
                print(f'Update Player to {self.player_name}')
            
            self.change_state("MainMenuState")

        # GAME buttons events
        elif event.ui_object_id == "game_panel.create_room_button":
            # cleanup
            game_state = self.current_state
            game_state.handle_create_room()
        elif event.ui_object_id == "game_panel.exit_button":
            # cleanup
            game_state = self.current_state
            game_state.game_panel.kill()
            del game_state

            # change back to main menu state
            self.change_state("MainMenuState")

        # QUIT button event
        elif event.ui_object_id == "quit_button":
            self.is_running = False