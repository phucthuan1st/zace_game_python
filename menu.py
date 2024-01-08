# menu.py
import pygame
import pygame_gui
from menu_buttons import create_button, handle_button_click, quit_game

def run_menu():
    pygame.init()

    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pygame GUI Menu")

    manager = pygame_gui.UIManager(window_size)

    clock = pygame.time.Clock()
    is_running = True

    button_positions = [(300, 200), (300, 300), (300, 400)]
    buttons = [create_button(manager, position, text) for position, text in zip(button_positions, ["Play", "Settings", "Quit"])]

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for button in buttons:
                        if event.ui_element == button:
                            handle_button_click(button, quit_game)

            manager.process_events(event)

        window.fill((255, 255, 255))
        manager.update(time_delta)
        manager.draw_ui(window)

        pygame.display.flip()

    pygame.quit()
