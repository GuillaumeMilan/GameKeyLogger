from pynput import keyboard
from pynput import mouse
import time
import threading

# Missing TAB, Space

# Global variable :/ 
logs = []
to_log_keys = [c for c in "azerdf&é\"'(-"]

lol_translate = {
	'a': "Q",
    'z': "W",
    'e': "E",
    'r': "R",
    'd': "D",
    'f': "F",
    '&': "1",
    'é': "2",
    '"': "3",
    '\'': "4",
    '(': "5",
    '-': "6",
    'è': "7"
}

dodge_game_translate = {
	'q': "Q",
    'e': "E",
    'd': "D",
}

translate = dodge_game_translate

print(to_log_keys)
is_logging = False
count = 0
debug = False
mouse_controller = mouse.Controller()
start_time = time.monotonic_ns()
mutex = threading.Lock()


# We don't log mouse moves (in league only clicks and keyboard matters)
def on_move(x, y):
    pass

# We log click and time
def on_click(x, y, button, pressed):
    global debug
    if debug:
        print('{0} at {1} button {2}'.format(
            'Pressed' if pressed else 'Released',
            (x, y), button))
    if pressed:
        try:
            logs.append(format_log(mouse_button(button)))
        except Exception:
            pass
    may_log()

def mouse_button(button):
    if button == mouse.Button.left:
        return "L Click"
    if button == mouse.Button.right:
        return "R Click"
    print("ERROR ON MOUSE")
    return ""

# We don't log scroll (no usage in league)
def on_scroll(x, y, dx, dy):
    pass

def on_press(key):
    global logs
    global debug
    if debug:   
        try:
            print('alphanumeric key {0} pressed => key {1} => type {2}'.format(key.char, key, type(key.char)))
        except AttributeError:
            print('special key {0} pressed'.format(key))
    try:
        logs.append(format_log(translate[key.char]))
    except Exception:
        pass
    may_log()

def clean_file():
    with open('log.txt', 'w') as f:
        f.write('')

def format_log(entry):
    global translate
    global mouse_controller
    (x, y) = mouse_controller.position
    return "{0}\t{1}\t{2}\t{3}".format(time.monotonic_ns() - start_time, x, y, entry)

def may_log():
    global logs
    if len(logs) >= 25:
        write_file()
lc = 0
def write_file():
    global logs
    global lc
    to_write = logs
    logs = []    
    with open('log.txt', 'a') as f:
        for log in to_write:
            lc += 1
            print("{0} {1}".format(lc, log))
            f.write(log)
            f.write('\n')

# For the moment type ESC for quit              
def on_release(key):
    if debug:
        print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        write_file()
        return False

# Script 

clean_file()
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
mouse_listener.start()
  
  
with keyboard.Listener(on_press = on_press,
              on_release = on_release) as keyboard_listener:
                     
    keyboard_listener.join()