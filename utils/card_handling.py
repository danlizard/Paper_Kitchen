import mtgsdk
import pickle
import os
import requests as req

from data.card import local_card
from config import card_image_root, card_info_root

class card_hub_class:
    def __init__(self,
        image_root:str = card_image_root,
        info_root:str = card_info_root):

        self.image_root = image_root
        if not os.path.exists(self.image_root):
            os.mkdir(self.image_root)
        self.info_root = info_root
        if not os.path.exists(self.info_root):
            os.mkdir(self.info_root)

        self.cards = dict()
        for name in os.listdir(info_root):
            if '.pkl' in name:
                self.cards[name.rstrip('.pkl')] = self._load_local(name)
    
    def _load_local(self, rawname:str):
        with open(self.info_root+rawname, 'rb') as src:
            return pickle.load(src)
    def _save_local(self, cardname:str):
        with open(self.info_root+cardname+'.pkl', 'wb') as trg:
            pickle.dump(self.cards[cardname], trg)
    def __del__(self):
        self.cleanup
        del self.cards 
    def cleanup(self):
        for name in self.cards:
            self._save_local(name)

    def local_from_api(self, card:mtgsdk.Card) -> local_card:
        newcard = local_card()
        for key in local_card.exposed_attributes:
            if card.__getattribute__(key):
                newcard.__setattr__(key, card.__getattribute__(key))
        name = newcard.name
        if "//" in name:
            if newcard.mana_cost:
                name = name.split(' // ')[0]
            else:
                name = name.split(' // ')[1]
        
        assert card.image_url, f"Tried to save imageless card {name}"
        img_data = req.get(card.image_url, verify=False).content
        with open(self.image_root+name+'.png', 'wb') as trg:
            trg.write(img_data)
        newcard.path = self.image_root+name+'.png' 
        self.cards[name] = newcard
        self._save_local(name)
        return newcard
    
    def get_image(self, name:str):
        return self.cards[name].get_image()

card_hub = card_hub_class()