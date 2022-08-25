import requests as req
import PySimpleGUI as sg
import cv2
import os
import time

import windows
import utils

running = True
updating = {"card":False, "list":False}
utils.initial_setup()

card_display_size = (254, 356)
cardsize_a4 = [620, 877]
listing_scale = 128

all_decks = os.listdir("./Paper_Kitchen_Decks/")
all_decks = [el.split('.')[0] for el in all_decks]
all_cards = os.listdir("./Paper_Kitchen_Cards/")
all_cards = [el.split('.')[0] for el in all_cards]

deckname = ''
cardlist = dict()
card_names_ordered = []

current_card_name = ''

central = windows.get_central(listing_scale, all_decks, all_cards)
central_window = sg.Window("Paper Kitchen v0.6", central)

while running:
	if not central_window.was_closed():
		event, values = central_window.read()
	else:
		break

	if event == "Exit":
		running = False
	elif event == "DECK_NAME":
		if deckname != '':
			if cardlist != dict():
				utils.save_card_info(cardlist, deckname)
				if deckname not in all_decks:
					all_decks.append(deckname)
					all_decks.sort()
				central_window["DECK_NAME"].update(values = all_decks)
		if values["DECK_NAME"]:
			deckname = values["DECK_NAME"]
			cardlist = dict()
			if deckname in all_decks:
				cardlist = utils.extract_card_info(f"./Paper_Kitchen_Decks/{values['DECK_NAME']}.dek")
			card_names_ordered = list(cardlist.keys())
			card_names_ordered.sort()
			print(f"selected {deckname.split('.')[0]}")
			central_window["DECK_NAME"].update(value = deckname)
			updating['list'] = True

	elif event == "SELECT_CARD":
		if values["SELECT_CARD"] in all_cards:
			current_card_name = values["SELECT_CARD"]
			current_card = cv2.imread(f"./Paper_Kitchen_Cards/{current_card_name}.png")
			updating['card'] = True
		else:
			success, current_card_name = utils.smart_search(values["SELECT_CARD"], all_cards)
			if success:
				current_card = cv2.imread(f"./Paper_Kitchen_Cards/{current_card_name}.png")
				updating['card'] = True
			else:
				central_window.perform_long_operation(lambda : utils.online_search(values["SELECT_CARD"]), "ONLINE_DONE")
	elif event == "ONLINE_DONE":
		success, current_card_name = values[event]
		if success:
			current_card = cv2.imread(f"./Paper_Kitchen_Cards/{current_card_name}.png")
			updating['card'] = True
			all_cards = os.listdir("./Paper_Kitchen_Cards/")
			all_cards = [el.split('.')[0] for el in all_cards]
			central_window['SELECT_CARD'].update(values = all_cards)
		else:
			print("Online Search Failed.")
			current_card_name = ''

	elif event == "Add":
		if current_card_name == '':
			continue
		if deckname == '':
			continue
		cardlist[current_card_name] = 1
		updating['list'] = True
		card_names_ordered = list(cardlist.keys())
		card_names_ordered.sort()

	elif event == "Export":
		utils.export(cardlist, cardsize_a4, name = deckname)

	elif "PLUS" in event:
		i = int(event.split('_')[1])
		cardlist[card_names_ordered[i]] += 1
		central_window[f"NUMBER_{i}"].update(cardlist[card_names_ordered[i]])
	elif "MINUS" in event:
		i = int(event.split('_')[1])
		cardlist[card_names_ordered[i]] -= 1
		if cardlist[card_names_ordered[i]] > 0:
			central_window[f"NUMBER_{i}"].update(cardlist[card_names_ordered[i]])
		else:
			cardlist.pop(card_names_ordered[i], None)
			card_names_ordered = list(cardlist.keys())
			card_names_ordered.sort()
			updating['list'] = True

	if updating['card']:
		imgbytes = cv2.imencode(".png", cv2.resize(current_card, card_display_size))[1].tobytes()
		central_window["RESULT"].update(data=imgbytes)
		updating['card'] = False
	if updating['list']:
		for i in range(len(card_names_ordered)):
			central_window[f"CARD_{i}"].update(value = card_names_ordered[i], visible=True)
			central_window[f"MINUS_{i}"].update(visible=True)
			central_window[f"NUMBER_{i}"].update(value = cardlist[card_names_ordered[i]], visible=True)
			central_window[f"PLUS_{i}"].update(visible=True)
		for i in range(len(card_names_ordered), listing_scale):
			central_window[f"CARD_{i}"].update(value = '', visible=False)
			central_window[f"MINUS_{i}"].update(visible=False)
			central_window[f"NUMBER_{i}"].update(value = 0, visible=False)
			central_window[f"PLUS_{i}"].update(visible=False)
		updating['list'] = False
	central_window = central_window.refresh()


if deckname != '':
	if cardlist != dict():
		utils.save_card_info(cardlist, deckname)

central_window.close()