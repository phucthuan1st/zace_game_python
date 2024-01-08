# menu_buttons.py
import pygame_gui

def create_button(position, text):
    return pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(position, (200, 50)),
        text=text,
        manager=None  # Manager will be set in the menu file
    )

def handle_button_click(button, action):
    if button == buttons[0]:
        print("Play button clicked")
        # Add play button functionality here
    elif button == buttons[1]:
        print("Settings button clicked")
        # Add settings button functionality here
    elif button == buttons[2]:
        print("Quit button clicked")
        action()

def quit_game():
    global is_running
    is_running = False
