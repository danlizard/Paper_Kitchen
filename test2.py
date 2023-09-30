from data.window import window_wrapper

import PySimpleGUI as sg
import time

from windows.providers import get_central

layout = get_central(128, [], [])

central = window_wrapper(layout, "Testing")
central.start()

def poll_window(window):
    if window.update:
        out = window.update
        window.update = None
        return out
    return None

def kill_window(window):
    print("window requested death")
    window.running = False
    window.window.write_event_value(("END_UPDATE", 0), None)
    window.join()

do = True
while do:
    out = poll_window(central)
    if out:
        event, values = out
        print(event, values)
        if event[0] == "KILLTHIS":
            kill_window(central)
            do = False
    time.sleep(0.01)