import PySimpleGUI as sg

import utils

sg.theme("LightGreen")

class DeckbuilderWindow:
	def __init__(card_list_length = 128):
		decktech_button = [sg.Combo([], k = "DECK_NAME", size=32, enable_events = True, bind_return_key = True, tooltip = "Deck selection; create a new deck by pressing Enter after typing in a name")]
		decktech_column = [decktech_button, [scalable_listing(listing_scale)], [sg.Sizer(h_pixels = 320, v_pixels = 0)]]
		searchbar_column = [[sg.Combo([], key="CARD_NAME",size=36, enable_events=True, bind_return_key = True, tooltip = "Local search & Online search powered by ScryFall"), sg.B("Add", tooltip = "Add card to deck")], [sg.Image(k="RESULT")], [sg.B("Export", tooltip = "Create printable deck sheets"), sg.B("Exit")]]
		self.layout = [[sg.Column(decktech_column), sg.VerticalSeparator(), sg.Column(searchbar_column),]]
	
	def activate(decks = [], cards = []):
		if decks:
			self.decks = decks
		if cards:
			self.cards = cards
		self.window = sg.Window("Paper Kitchen v0.6", self.layout)
		central_window["DECK_NAME"].update(values = self.decks)
		central_window["CARD_NAME"].update(values = self.cards)
	
	def update_elements(element_keys, element_values):
		if isinstance(element_keys, str):
			element_keys = [element_keys]
			element_values = [element_values]
		for i, (key, values) in enumerate(zip(element_keys, element_values)):
			self.window[key].update(value)
		
	def card_listing(scale):
	    listing = [[sg.T(f"", size=36, k=f"CARD_{i}", visible=False), sg.B("-", size=1, k=f"MINUS_{i}", visible=False), sg.T("0", size=2, k=f"NUMBER_{i}", visible=False), sg.B("+", size=1, k=f"PLUS_{i}", visible=False)] for i in range(scale+1)]
	    listing[-1] = [sg.Sizer(h_pixels = 380, v_pixels = 400)]
	    return sg.Column(listing, scrollable=True, vertical_scroll_only=True)