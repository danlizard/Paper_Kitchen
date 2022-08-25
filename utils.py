import requests as req
import cv2
import numpy as np
import os

a4xbase = 2480
a4ybase = 3508

def initial_setup():
	available = os.listdir()
	if "Paper_Kitchen_Cards" not in available:
		os.mkdir("Paper_Kitchen_Cards")
	if "Paper_Kitchen_Decks" not in available:
		os.mkdir("Paper_Kitchen_Decks")

def clean_name(name):
	name = name.split('/')[-1]
	name = name.split('\\')[-1]
	name = name.split('.')[0]
	return name

def clean_code(string):
	string = "'".join(string.split("&#39;"))
	string = "-".join(string.split("//"))
	
	return string

def extract_card_info(path):
	cardlist = dict()
	with open(path, 'r') as src:
		for line in src.readlines():
			name, count = line.split('__')
			cardlist[name] = int(count)
	return cardlist

def save_card_info(cards, name):
	with open(f"Paper_Kitchen_Decks/{name}.dek", 'w') as trg:
		for card in cards.keys():
			trg.write(card+'__'+str(cards[card])+'\n')

def export(cardlist, base_cardsize, name="latest_", dpi = 600):
	global a4xbase, a4ybase
	scaler = dpi//300
	a4x, a4y = a4xbase*scaler, a4ybase*scaler
	pos = 0
	cardsize = []
	for el in base_cardsize:
		cardsize.append(el*scaler)
	side = 4 # ADD VARIABILITY
	
	card_copies = []
	for card in cardlist.keys():
		for i in range(cardlist[card]):
			card_copies.append(card)
	i = 1
	for card in card_copies:
		if pos == side*side:
			pos = 0
			cv2.imwrite(f'./Paper_Kitchen_Decks/{name} - Sheet {i}.png', sheet)
			i +=1
		if pos == 0:
			sheet = np.zeros((a4y, a4x, 3), dtype=np.uint8)
			sheet.fill(255)
		h_pos = pos%side
		v_pos = pos//side
		raw_card_image = cv2.imread(f"./Paper_Kitchen_Cards/{card}.png")
		card_image = cv2.resize(raw_card_image, (cardsize[0], cardsize[1]))
		sheet[cardsize[1]*v_pos:cardsize[1]*(v_pos+1), cardsize[0]*h_pos:cardsize[0]*(h_pos+1), :] = card_image
		pos +=1
	cv2.imwrite(f'./Paper_Kitchen_Decks/{name} - Sheet {i}.png', sheet)

def smart_search(name, all_cards): #not really smart yet
	for el in all_cards:
		if name in el:
			return True, el
	return False, None

def online_search(name, engine = "scryfall.com"):
	if engine == "scryfall.com":
		info = req.get(f"https://{engine}/search?q={name}&as=checklist&unique=cards")
	if not info.ok:
		return False, "Engine not OK"
	elif engine == "scryfall.com":
		is_profile = False # if 1 card only, search for class="card-profile" - src right after
		is_list = False
		card_list = dict() #search for <tbody>, for data-card-image-front and the next href after it for every card

		action_do = False
		link = None
		name = None
		i = 0
		content = []
		for raw in info.iter_lines():
			line = raw.decode('UTF-8')
			if '<div class="card-profile">' in line:
				is_profile = True
			if '<table class="checklist" id="js-checklist">' in line:
				is_list = True
			if is_list:
				if 'data-card-image-front=' in line:
					link = (line.split('data-card-image-front=')[1]).split('?')[0][1:]
					action_do = True
				if '<td class="ellipsis"><a lang="en" href="' in line and action_do:
					name = (line.split('</a>')[0]).split('>')[-1]
					card_list[name] = link
					action_do = False
					print(f"Found name {name} at {link}")
			if is_profile:
				if 'src="' in line:
					link = (line.split('src="')[1]).split('?')[0]
					action_do = True
				if '<' not in line and line !='' and action_do:
					name = line.lstrip().rstrip()
					card_list[name] = link
					action_do = False
					print(f"Found name {name} at {link}")
					break
		info.close()
		del info
		if link == None or name == None:
			return False, "No Card Found"
		for name in list(card_list.keys()):
			imagesrc = req.get(card_list[name])
			if not imagesrc.ok:
				return False, "Image Download not OK"
			with open(f'./Paper_Kitchen_Cards/{clean_code(name)}.png', 'wb') as trg:
				for chunk in imagesrc:
					trg.write(chunk)
			imagesrc.close()
		return True, clean_code(name)