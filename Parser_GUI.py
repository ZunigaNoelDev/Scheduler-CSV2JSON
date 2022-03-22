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

def NewEntry(parent, key, labelText, entryText, buttonText, method, row, col, pad_x, pad_y, entryWidth=12, row_offset=0, col_offset=1, hasButton=True):
	widgets[key] = {"label": Label(parent, text=labelText), "entry": Entry(parent, width=entryWidth)}

	widgets[key]["label"].grid(row=row, column=col, 
		sticky="w", columnspan=1,
		padx=(parent.winfo_width()*pad_x,0),
		pady=(parent.winfo_width()*pad_y,0))

	widgets[key]["entry"].insert(0, entryText)
	widgets[key]["entry"].grid(row=row+row_offset, column=col+col_offset, 
		sticky="w", columnspan=1,
		padx=(0,0),
		pady=(parent.winfo_width()*pad_y,0))

	if hasButton:
		widgets[key]["button"] = Button(parent, text=buttonText, command=method)
		widgets[key]["button"].grid(row=row+row_offset, column=col+col_offset+1, 
			sticky="e", columnspan=1,
			padx=(0,parent.winfo_width()*pad_x),
			pady=(parent.winfo_width()*pad_y,0))

	return widgets[key]

def NewOptionMenu(parent, key, labelText, optionList, curr_selection, buttonText, method, row, col, pad_x, pad_y, width, row_offset=0, col_offset=1):
	widgets[key] = {"var": StringVar(parent, value=curr_selection), "label": Label(parent, text=labelText), "button": Button(parent, text=buttonText, command=method)}
	widgets[key]["options"] = OptionMenu(parent, widgets[key]["var"], *optionList)

	widgets[key]["label"].grid(row=row, column=col, 
		sticky="w", columnspan=1,
		padx=(parent.winfo_width()*pad_x,0),
		pady=(parent.winfo_width()*pad_y,0))

	widgets[key]["options"].config(width=width)
	widgets[key]["options"].grid(row=row+row_offset, column=col+col_offset, 
		sticky="w", columnspan=1,
		padx=(0,0),
		pady=(parent.winfo_width()*pad_y,0))
	
	widgets[key]["button"].grid(row=row+row_offset, column=col+col_offset+1, 
		sticky="e", columnspan=1,
		padx=(0,parent.winfo_width()*pad_x),
		pady=(parent.winfo_width()*pad_y,0))

	return widgets[key]

def StepOne():
	# widgets["Location"]["button"]["text"] = "Update"
	path = os.getcwd() + "\\Files"
	if not "Courses" in widgets.keys():
		courses_widget = NewButton(
			parent=root,
			key="Courses",
			labelText=f"1.) Courses",
			buttonText="Load",
			method=lambda:LoadFile("Open a JSON File", path, (('JSON files', '*.json'),), StepTwo, key="Courses"),
			pad_x=0.05, pad_y=0.05,
			row=1, col=0)
	widgets["Courses"]["label"].focus()
	if os.path.exists(path+"\\courses.json"):
		StepTwo(path+"\\courses.json")


def StepTwo(filepath):
	path = os.getcwd() + "\\Files"
	filename = filepath.split("\\")[-1]
	widgets["Courses"]["label"]["text"] = f"1.) {filename}"
	widgets["Courses"]["button"]["text"] = "Change"

	if not "Locations" in widgets.keys():
		locations_widget = NewButton(
			parent=root,
			key="Locations",
			labelText=f"2.) Locations",
			buttonText="Load",
			method=lambda:LoadFile("Open a JSON File", os.getcwd() + "/Files/", (('JSON files', '*.json'),), StepThree, key="Locations"),
			pad_x=0.05, pad_y=0.05,
			row=2, col=0)
	if os.path.exists(path+"\\locations.json"):
		StepThree(path+"\\locations.json")


def StepThree(filepath):
	path = os.getcwd() + "\\Files"
	filename = filepath.split("\\")[-1]
	widgets["Locations"]["label"]["text"] = f"2.) {filename}"
	widgets["Locations"]["button"]["text"] = "Change"
	locations = GetJKeys(filepath)

	CSV_Widget = NewButton(
		parent=root,
		key="CSV",
		labelText="3.) CSV File",
		buttonText="Load",
		method=lambda:LoadFile("Open a CSV File", os.getcwd() + "/Files/", (('CSV files', '*.csv'),), StepFour, key="Schedule"),
		pad_x=0.05, pad_y=0.05,
		row=3, col=0)
	loc = None
	for location in locations:
		if os.path.exists(path+f"\\{location}.csv"):
			loc = location
			files["Schedule"] = path+f"\\{location}.csv"
			StepFour(path+f"\\{location}.csv", locations)
			break
	if not loc and os.path.exists(path+f"\\schedule.csv"):
		files["Schedule"] = path+"\\schedule.csv"
		StepFour(path+f"\\schedule.csv", locations)


def StepFour(filepath, locations):
	filename = filepath.split("\\")[-1]
	widgets["CSV"]["label"]["text"] = f"3.) {filename}"
	widgets["CSV"]["button"]["text"] = "Change"

	location = filename.split(".")[0]
	if location not in locations:
		location="San Diego"
	if "Location" in widgets.keys():
		current = widgets["Location"]["entry"].get()
		widgets["Location"]["entry"].delete(0, len(current))
		widgets["Location"]["entry"].insert(0, location)
	else:
		location_widget = NewOptionMenu(
			parent=root,
			key="Location",
			labelText=f"4.) Location:",
			optionList=locations,
			curr_selection=location,
			buttonText="Confirm",
			method=StepFive,
			pad_x=0.05, pad_y=0.05,
			row=4, col=0, width=12)
	widgets["Location"]["options"].focus()


def StepFive():
	widgets["Location"]["button"]["text"] = "Change"
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
			row=5, col=0)
		
		# names_col_l, names_col = NewEntry(root, "Column Containing Course Names", 4, 1)
		# dates_first_l, dates_first = NewEntry(root, "Column Containing First Date", 5, 1)
		# dates_last_l, dates_lase = NewEntry(root, "Column Containing Last Date", 6, 1)
		# price__5D_col_l, price__5D_col = NewEntry(root, "Column Containing 5 Day Price", 7, 1)
		# price__4D_col_l, price__4D_col = NewEntry(root, "Column Containing 4 Day Price", 8, 1)


def StepSix():
	widgets["Weeks Row"]["button"]["text"] = "Change"
	if not "Start Row" in widgets.keys():
		schedule_row_start = NewEntry(
			parent=root,
			key="Start Row",
			labelText="6.) First Schedule Row",
			entryText=[val if (val:=GetScheduleRows(files["Schedule"], "open")[0]+1) > 0 else -1][0],
			entryWidth=len(str(val)) if val > 0 else 2,
			buttonText="Confirm",
			method=StepSeven,
			hasButton=False,
			pad_x=0.05, pad_y=0.05,
			row=6, col=0)
		schedule_row_end = NewEntry(
			parent=root,
			key="End Row",
			labelText="      Last Schedule Row",
			entryText=[val if (val:=GetScheduleRows(files["Schedule"], "open")[1]+1) > 0 else -1][0],
			entryWidth=len(str(val)) if val > 0 else 2,
			buttonText="Confirm",
			method=StepSeven,
			pad_x=0.05, pad_y=0.00,
			row=7, col=0)


def StepSeven():
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


def GetScheduleRows(filepath, keyword):
	with open(filepath, "r") as read_obj:
		reader = csv.reader(read_obj)
		start_row = -1
		end_row = -1
		keyword_count = 0
		first = True
		for index,row in enumerate(reader):
			text = ''.join(row)
			count = text.count(keyword)
			if count > 0 and first:
				start_row = index
				first = False
			elif count >= keyword_count:
				keyword_count = keyword_count
				end_row = index

	return start_row, end_row

def GetJKeys(filepath):
	with open(filepath) as jsonFile:
		data = json.load(jsonFile)
		return [entry["name"] for entry in data]

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
root.update_idletasks()

widgets = {}
StepOne()
root.mainloop()