import pygame
import pygame_gui
from menu_buttons import create_button, handle_button_click, quit_game

def run_menu():
    pygame.init()

    # Control running state
    global is_running
    is_running = True

    window_size = (900, 900)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Zace Tank Battle")

    manager = pygame_gui.UIManager(window_size)

    clock = pygame.time.Clock()

    button_width = 0.2  # 20% of window width
    button_height = 0.05  # 5% of window height
    button_margin = 0.02  # 2% of window height

    # Calculate the starting y-coordinate for the first button
    start_y = (window_size[1] - (button_height + button_margin) * len(["Play", "Settings", "Quit"])) // 2

    button_positions = [(0.4 * window_size[0], start_y + i * (button_height * window_size[1] + button_margin * window_size[1])) for i in range(len(["Play", "Settings", "Quit"]))]
    buttons = [create_button(manager, position, text) for position, text in zip(button_positions, ["Play", "Settings", "Quit"])]

    # Load logo
    logo_image = pygame.image.load("assets/zacetankbattle-logo-transparent.png")
    original_logo_rect = logo_image.get_rect()

    # Scale the logo based on window size
    scaling_factor = 0.15  # Adjust as needed
    scaled_logo = pygame.transform.scale(logo_image, (int(original_logo_rect.width * scaling_factor), int(original_logo_rect.height * scaling_factor)))
    logo_rect = scaled_logo.get_rect()
    logo_position = ((window_size[0] - logo_rect.width) // 2, 50)  # Adjust the vertical position as needed

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

        # Draw logo
        window.blit(scaled_logo, logo_position)

        manager.update(time_delta)
        manager.draw_ui(window)

        pygame.display.flip()

    pygame.quit()