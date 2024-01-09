import pygame
import pygame_gui
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SERVER_ADDRESS

from helpers.random_name_generator import generate_random_name
from states.state_manager import StateManager

def main():
    pygame.init()
    pygame.display.set_caption("Zace Tank Battle")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    volume_percent = 50
    server_address = SERVER_ADDRESS
    player_name = generate_random_name()

    state_manager = StateManager(ui_manager, player_name, volume_percent, server_address)

    # Initialize Pygame mixer for sound
    pygame.mixer.init()
    soundtrack = pygame.mixer.Sound("assets/Soviet_March.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            state_manager.handle_events(event)

        # Set the soundtrack's volume based on volume_percent
        soundtrack.set_volume(state_manager.volume_percent / 100)

        # Play the soundtrack in a loop (if not already playing)
        if not pygame.mixer.get_busy():
            soundtrack.play(-1)

        state_manager.update(float(clock.tick(FPS) / 1000))
        state_manager.render(screen)

        running = state_manager.is_running

        pygame.display.update()

if __name__ == "__main__":
    main()
