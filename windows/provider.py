import PySimpleGUI as sg

from windows.subelements import scalable_listing

def get_central(listing_scale, current_decks, available_cards):
	decktech_button = [sg.Combo(current_decks, k = "DECK_NAME", size=32, enable_events = True, bind_return_key = True, tooltip = "Deck selection; create a new deck by pressing Enter after typing in a name")]
	decktech_column = [decktech_button, [scalable_listing(listing_scale)], [sg.Sizer(h_pixels = 320, v_pixels = 0)]]
	searchbar_column = [[sg.Combo(available_cards, key="SELECT_CARD",size=36, enable_events=True, bind_return_key = True, tooltip = "Local search & Online search powered by ScryFall"), sg.B("Add", tooltip = "Add card to deck")],
						[sg.Image(k="RESULT")], [sg.B("Export", tooltip = "Create printable deck sheets"), sg.B("Exit", key="KILLTHIS")]]
	layout = [[sg.Column(decktech_column),
 			  sg.VerticalSeparator(),
     		  sg.Column(searchbar_column),]]
	return layout