# menu_buttons.py
import pygame
import pygame_gui

def create_button(manager, position, text):
    return pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(position, (200, 50)),
        text=text,
        manager=manager
    )

def handle_button_click(button, action):
    if button.text == "Play":
        print("Play button clicked")
        # Add play button functionality here
    elif button.text == "Settings":
        print("Settings button clicked")
        # Add settings button functionality here
    elif button.text == "Quit":
        print("Quit button clicked")
        action()

def quit_game():
    print("Quitting game...")
    global is_running
    is_running = False
