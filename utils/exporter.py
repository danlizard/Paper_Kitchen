import cv2
import numpy as np
from threading import Thread

from data.deck import deck
from config import default_export_config

a4xbase = 2480
a4ybase = 3508

class exporter_thread(Thread):
	def __init__(self, deck_dict:dict, config:dict, export_root:str, name="latest_", dpi = 600):
		Thread.__init__(self)
		scale_factor = dpi//300
		self.path = export_root
		self.x_total = config['xbase']*scale_factor
		self.y_total = config['ybase']*scale_factor
		self.x_card = config['xcard']*scale_factor
		self.y_card = config['ycard']*scale_factor
		self.sides = config['side_n']
		self.finished = False
		self.name = name

		self.card_copies = []
		for card in deck_dict:
			for i in range(deck_dict[card]['count']):
				self.card_copies.append(card)

	def run(self):
		pos = 0
		i = 1
		for card in self.card_copies:
			if pos == self.sides**2:
				pos = 0
				cv2.imwrite(f'{self.path}{self.name} - sheet {i}.png', sheet)
				i +=1
			if pos == 0:
				sheet = np.full((self.x_total, self.y_total, 3), 255, dtype=np.uint8)
			h_pos = pos%self.sides
			v_pos = pos//self.sides
			card_image = cv2.resize(card.get_image(), (self.x_card, self.y_card), interpolation=cv2.INTER_CUBIC)
			sheet[self.x_card*v_pos:self.x_card*(v_pos+1), self.y_card*h_pos:self.y_card*(h_pos+1), :] = card_image
			pos +=1
		self.finished = True


def begin_export(deck:deck, config:dict, export_root:str, dpi:int = 600):
	exporter = exporter_thread(deck.cards, config, export_root, name=deck.name, dpi=dpi)
	exporter.start()
	return exporter