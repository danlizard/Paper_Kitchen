import cv2

from config import card_display_size

class local_card:
    exposed_attributes = ['name', 'mana_cost', 'cmc', 'types', 'rarity', 'power', 'toughness']
    name = None
    path = None
    mana_cost = None
    cmc = 0
    types = None
    rarity = None
    power = None
    toughness = None

    def __init__(self, **attributes) -> None:
        for key in attributes:
            self.__setattr__(key, attributes[key])

    def __repr__(self) -> str:
        return self.name
    
    def __lt__(self, other):
        return self.cmc < other.cmc
    def __gt__(self, other):
        return self.cmc > other.cmc
    def __eq__(self, other):
        return self.cmc == other.cmc

    def get_image(self):
        raw = cv2.imread(self.path)
        return cv2.imencode(".png", cv2.resize(raw, card_display_size))[1].tobytes()