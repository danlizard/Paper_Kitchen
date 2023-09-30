import PySimpleGUI as sg

def scalable_listing(scale):
	listing = [[sg.T(f"", size=36, k=f"CARD_{i}", visible=False), sg.B("-", size=1, k=f"MINUS_{i}", visible=False),
						sg.T("0", size=2, k=f"NUMBER_{i}", visible=False), sg.B("+", size=1, k=f"PLUS_{i}", visible=False)] for i in range(scale+1)]
	listing[-1] = [sg.Sizer(h_pixels = 380, v_pixels = 400)]
	return sg.Column(listing, scrollable=True, vertical_scroll_only=True)