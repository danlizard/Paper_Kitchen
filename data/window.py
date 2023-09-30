from threading import Thread
import PySimpleGUI as sg

# EVENTS #
# (name, code) #
# code 0: event was emitted by core #
# code 1: event was emitted by user in window #
# code 2: event was emitted by window autonomously #

class window_wrapper(Thread):
    def __init__(self, layout:list, name:str):
        Thread.__init__(self)
        self.name = name
        self.layout = layout
        self.running = False
        self.update = None

    def run(self):
        self.running = True
        self.window = sg.Window(self.name, self.layout)
        while self.running:
            update = self.window.read()
            if update[0] == sg.WIN_CLOSED:
                self.update = (("KILLTHIS", 2), update[1])
            elif update[0][1]: # if not emitted by core
                if "INTERNAL" in update[0][1]:
                    self.update = ((update[0], 2), update[1])
                else:
                    self.update = ((update[0], 1), update[1])
            self.window = self.window.refresh()
        self.window.close()