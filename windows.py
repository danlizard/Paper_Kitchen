import PySimpleGUI as sg

import utils

sg.theme("LightGreen")

def scalable_listing(scale):
	listing = [[sg.T(f"", size=36, k=f"CARD_{i}", visible=False), sg.B("-", size=1, k=f"MINUS_{i}", visible=False),
						sg.T("0", size=2, k=f"NUMBER_{i}", visible=False), sg.B("+", size=1, k=f"PLUS_{i}", visible=False)] for i in range(scale+1)]
	listing[-1] = [sg.Sizer(h_pixels = 380, v_pixels = 400)]
	return sg.Column(listing, scrollable=True, vertical_scroll_only=True)

"""
def run_deck_selector():
	layout = [[sg.T('Choose a deck file, or name a new one below'), sg.FileBrowse(key="FILE", initial_folder='./Paper_Kitchen_Decks/', file_types=(("DEK files", "*.dek"),))],
	[sg.In(key='NEW_FILE'), sg.B("OK")]]
	return sg.Window('Selector Window', layout).read(close=True)
"""

def get_central(listing_scale, current_decks, available_cards):
	decktech_button = [sg.Combo(current_decks, k = "DECK_NAME", size=32, enable_events = True, bind_return_key = True, tooltip = "Deck selection; create a new deck by pressing Enter after typing in a name")]
	decktech_column = [decktech_button, [scalable_listing(listing_scale)], [sg.Sizer(h_pixels = 320, v_pixels = 0)]]
	searchbar_column = [[sg.Combo(available_cards, key="SELECT_CARD",size=36, enable_events=True, bind_return_key = True, tooltip = "Local search & Online search powered by ScryFall"), sg.B("Add", tooltip = "Add card to deck")],
						[sg.Image(k="RESULT")], [sg.B("Export", tooltip = "Create printable deck sheets"), sg.B("Exit")]]
	layout = [[sg.Column(decktech_column),
 			  sg.VerticalSeparator(),
     		  sg.Column(searchbar_column),]]
	return layout