import time

from config import full

from utils.card_handling import card_hub
from utils.deck_handling import deck_hub

from data.window import window_wrapper
from windows import window_provider

class app_core:
    def __init__(self, configs = full) -> None:
        self.configs = configs
        self.running = False

        self.cardhub = card_hub
        self.deckhub = deck_hub
        
        central_deck_window = window_wrapper(providers.get_central(128, [], []), "Paper Kitchen 1.-1")
        central_deck_window.start()
        self.window_processes = {"central": central_deck_window}

    def _poll_window(self, wid:str) -> tuple|None:
        assert isinstance(wid, str)
        wobj = self.window_processes[wid]
        out = None
        if wobj.update:
            out = wobj.update
            wobj.update = None
        return out
    
    def _kill_window(self, wid:str) -> None:
        assert isinstance(wid, str)
        wobj = self.window_processes[wid]
        wobj.running = False
        wobj.window.write_event_value(("END_UPDATE", 0), None)
        wobj.join()
        del self.window_processes[wid]

    def loop(self) -> None:
        self.running = True
        while self.running:
            for wname in self.window_processes:
                out = self._poll_window(wname)
                if not out:
                    time.sleep(0.01)
                    continue
                event, values = out
                print(event, values)
                if event[0] == "KILLTHIS":
                    self._kill_window(wname)
                else:

                if not self.window_processes:
                    self.running = False
                    break
                time.sleep(0.01)

if __name__ == "__main__":
    core = app_core()
    core.loop()