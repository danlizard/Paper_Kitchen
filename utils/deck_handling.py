import os
import pickle

from data.deck import deck
from utils.exporter import begin_export
from config import deck_export_root, deck_info_root, default_export_config

class deck_hub_class:
    def __init__(self,
        info_root = deck_info_root,
        export_root = deck_export_root):
        
        self.info_root = info_root
        if not os.path.exists(self.info_root):
            os.mkdir(self.info_root)
        self.export_root = export_root
        if not os.path.exists(self.export_root):
            os.mkdir(self.export_root)
        
        self.decks = dict()
        for name in os.listdir(info_root):
            if '.pkl' in name:
                self.decks[name.rstrip('.pkl')] = self._load_local(name)
        
        self.current_deck = None
    
    def _load_local(self, rawname:str):
        with open(self.info_root+rawname, 'rb') as src:
            return pickle.load(src)
    def _save_local(self, deckname:str):
        with open(self.info_root+deckname+'.pkl', 'wb') as trg:
            pickle.dump(self.decks[deckname], trg)
    def __del__(self):
        self.cleanup
        del self.decks 
    def cleanup(self):
        for name in self.decks:
            self._save_local(name)
    
    def select_deck(self, name:str):
        assert name in self.decks, f"Cannot select: no deck named {name}"
        self.current_deck = self.decks[name]
    def create_deck(self, name:str):
        self.decks[name] = deck(name)
        self.select_deck(name)
    def remove_deck(self, name:str):
        assert name in self.decks, f"Cannot delete: no deck named {name}"
        if self.current_deck.name == name:
            self.current_deck = None
        del self.decks[name]
        os.remove(self.info_root+name+'pkl')

    def export_deck(self, name:str, export_config:dict=default_export_config):
        assert name in self.decks, f"Cannot export: no deck named {name}"
        return begin_export(self.decks[name], export_config, self.export_root)

deck_hub = deck_hub_class()