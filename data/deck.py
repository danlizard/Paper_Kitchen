from data.card import local_card

class deck:
    def __init__(self, name:str) -> None:
        self.name = name
        self.cards = dict()

    def __repr__(self) -> str:
        return self.name
    def __len__(self) -> int:
        return sum([self[name]['count'] for name in self])
    def __getitem__(self, name:str) -> local_card:
        if name not in self.cards:
            raise KeyError
        return self[name]
    def __setitem__(self, name:str, card:local_card):
        name = card.name
        self[name] = {'item':card, 'count':1}
    def __contains__(self, card:str|local_card):
        name = card
        if isinstance(card, local_card):
            name = card.name
        if name in self.cards:
            return True
        return False
        
    def add_card(self, card:local_card) -> None:
        if card.name not in self.cards:
            self[card.name] = {'item':card, 'count':0}
        self[card.name]['count'] += 1
    
    def remove_card(self, card:local_card|str) -> None:
        name = card
        if isinstance(card, local_card):
            name = card.name
        if name not in self:
            return
        self.cards[name]['count'] -= 1
        if not self[name]['count']:
            del self[name]
        
    def get_image(self, name:str):
        assert name in self, f"Cannot get image: {name} not in {self.name}"
        return self[name].get_image()