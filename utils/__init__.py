import os

def initial_setup():
	available = os.listdir()
	if "Paper_Kitchen_Cards" not in available:
		os.mkdir("Paper_Kitchen_Cards")
	if "Paper_Kitchen_Decks" not in available:
		os.mkdir("Paper_Kitchen_Decks")