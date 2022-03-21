import os, json, datetime, requests, time, csv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

def InitializeRoot(title, width_ratio, height_ratio, x_pos=0, y_pos=0, columns=1):
	root = Tk()
	root.title(title)
	root.resizable(False, False)

	SCREEN_WIDTH = root.winfo_screenwidth()
	SCREEN_HEIGHT = root.winfo_screenheight()
	x_offset = SCREEN_WIDTH * x_pos if x_pos < 1 else x_pos
	y_offset = SCREEN_HEIGHT * y_pos if y_pos < 1 else y_pos 

	root.geometry((f"{int(SCREEN_WIDTH * width_ratio)}x{int(SCREEN_HEIGHT * height_ratio)}"))
	root.geometry((f"+{int(x_offset)}+{int(y_offset)}"))
	for i in range(columns-1):
		root.columnconfigure(i, weight=1)
	return root

def NewButton(parent, key, labelText, buttonText, method, row, col, pad_x, pad_y, row_offset=0, col_offset=1):
	widgets[key] = {"label": Label(parent, text=labelText), "button": Button(parent, text=buttonText, command=method)}

	widgets[key]["label"].grid(row=row, column=col, 
		sticky="w", columnspan=2,
		padx=(parent.winfo_width()*pad_x,0),
		pady=(parent.winfo_width()*pad_y,0))

	widgets[key]["button"].grid(row=row+row_offset, column=col+col_offset, 
		sticky="e", columnspan=2,
		padx=(0,parent.winfo_width()*pad_x),
		pady=(parent.winfo_width()*pad_y,0))

	return widgets[key]

def NewEntry(parent, key, labelText, entryText, buttonText, method, row, col, pad_x, pad_y, entryWidth=12, row_offset=0, col_offset=1):
	widgets[key] = {"label": Label(parent, text=labelText), "entry": Entry(parent, width=entryWidth), "button": Button(parent, text=buttonText, command=method)}

	widgets[key]["label"].grid(row=row, column=col, 
		sticky="w", columnspan=1,
		padx=(parent.winfo_width()*pad_x,0),
		pady=(parent.winfo_width()*pad_y,0))

	widgets[key]["entry"].insert(0, entryText)
	widgets[key]["entry"].grid(row=row+row_offset, column=col+col_offset, 
		sticky="w", columnspan=1,
		padx=(0,0),
		pady=(parent.winfo_width()*pad_y,0))
	
	widgets[key]["button"].grid(row=row+row_offset, column=col+col_offset+1, 
		sticky="e", columnspan=1,
		padx=(0,parent.winfo_width()*pad_x),
		pady=(parent.winfo_width()*pad_y,0))

	return widgets[key]

def StepOne():
	CSV_Widget = NewButton(
		parent=root,
		key="CSV",
		labelText="1.) CSV File",
		buttonText="Load",
		method=lambda:LoadFile("Open a CSV File", "/Downloads", (('CSV files', '*.csv'),), StepTwo, key="Schedule"),
		pad_x=0.09, pad_y=0.05,
		row=0, col=0)

def StepTwo(filepath):
	filename = filepath.split("/")[-1]
	widgets["CSV"]["label"]["text"] = f"1.) {filename}"
	widgets["CSV"]["button"]["text"] = "Change"

	location = filename.split(".")[0]

	if "Location" in widgets.keys():
		current = widgets["Location"]["entry"].get()
		widgets["Location"]["entry"].delete(0, len(current))
		widgets["Location"]["entry"].insert(0, location)
	else:
		location_widget = NewEntry(
			parent=root,
			key="Location",
			labelText=f"2.) Location:",
			entryText=location,
			buttonText="Confirm",
			method=StepThree,
			pad_x=0.05, pad_y=0.05,
			row=1, col=0)
	widgets["Location"]["entry"].focus()

def StepThree():
	widgets["Location"]["button"]["text"] = "Update"
	if not "Courses" in widgets.keys():
		courses_widget = NewButton(
			parent=root,
			key="Courses",
			labelText=f"3.) Courses",
			buttonText="Load",
			method=lambda:LoadFile("Open a JSON File", "/Downloads", (('JSON files', '*.json'),), StepFour, key="Courses"),
			pad_x=0.05, pad_y=0.05,
			row=2, col=0)
	widgets["Courses"]["label"].focus()

def StepFour(filepath):
	filename = filepath.split("/")[-1]
	widgets["Courses"]["label"]["text"] = f"3.) {filename}"
	widgets["Courses"]["button"]["text"] = "Change"

	if not "Locations" in widgets.keys():
		locations_widget = NewButton(
			parent=root,
			key="Locations",
			labelText=f"4.) Locations",
			buttonText="Load",
			method=lambda:LoadFile("Open a JSON File", "/Downloads", (('JSON files', '*.json'),), StepFive, key="Locations"),
			pad_x=0.05, pad_y=0.05,
			row=3, col=0)

def StepFive(filepath):
	filename = filepath.split("/")[-1]
	widgets["Locations"]["label"]["text"] = f"4.) {filename}"
	widgets["Locations"]["button"]["text"] = "Change"

	if not "Weeks Row" in widgets.keys():
		weeks_row = NewEntry(
			parent=root,
			key="Weeks Row",
			labelText="5.) Dates Row",
			entryText=GetWeeksRow(files["Schedule"])+1,
			entryWidth=2,
			buttonText="Confirm",
			method=StepSix,
			pad_x=0.05, pad_y=0.05,
			row=4, col=0)
		# courses_row_first_l, courses_row_first = NewEntry(root, "Row Containing First Course", 2, 1)
		# courses_row_last_l, courses_row_last = NewEntry(root, "Row Containing Last Course", 3, 1)
		# names_col_l, names_col = NewEntry(root, "Column Containing Course Names", 4, 1)
		# dates_first_l, dates_first = NewEntry(root, "Column Containing First Date", 5, 1)
		# dates_last_l, dates_lase = NewEntry(root, "Column Containing Last Date", 6, 1)
		# price__5D_col_l, price__5D_col = NewEntry(root, "Column Containing 5 Day Price", 7, 1)
		# price__4D_col_l, price__4D_col = NewEntry(root, "Column Containing 4 Day Price", 8, 1)

def StepSix():
	for key in widgets:
		print(widgets[key])
	for file in files:
		print(files[file])
	pass


def GetWeeksRow(filepath):
	with open(filepath, "r") as read_obj:
		reader = csv.reader(read_obj)
		dates_row = 0
		dates_count = 0
		for index,row in enumerate(reader):
			text = ''.join(row)
			count = text.count("/")
			if count > dates_count:
				dates_count = count
				dates_row = index
	return dates_row


def LoadFile(title, dir, filetypes, nextstep, key=None):
	filepath = fd.askopenfilename(
		title=title,
		initialdir=dir,
		filetypes=(filetypes)
	)
	if filepath:
		if key:
			files[key] = filepath
		nextstep(filepath)

files = {}
# Initializing root window with a custom method to simplify customization
root = InitializeRoot(
	title="Spreadsheet Schedule Parser",
	width_ratio=.25,
	height_ratio=.5,
	x_pos=.70,
	y_pos=.25,
	columns=3)

widgets = {}

# Load CSV Widget
StepOne()

# Text boxes for inputting relevant cells
# weeks_row_l, weeks_row = NewTextInput(root, "Row Containing Week Dates", 1, 1)
# courses_row_first_l, courses_row_first = NewTextInput(root, "Row Containing First Course", 2, 1)
# courses_row_last_l, courses_row_last = NewTextInput(root, "Row Containing Last Course", 3, 1)
# names_col_l, names_col = NewTextInput(root, "Column Containing Course Names", 4, 1)
# dates_first_l, dates_first = NewTextInput(root, "Column Containing First Date", 5, 1)
# dates_last_l, dates_lase = NewTextInput(root, "Column Containing Last Date", 6, 1)
# price__5D_col_l, price__5D_col = NewTextInput(root, "Column Containing 5 Day Price", 7, 1)
# price__4D_col_l, price__4D_col = NewTextInput(root, "Column Containing 4 Day Price", 8, 1)

# root.after(3000,lambda:root.destroy())
root.mainloop()