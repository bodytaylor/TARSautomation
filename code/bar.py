import time
import pyautogui
import webbrowser
import openpyxl

# Function to load Excel file and select the sheet
def load_excel_file(file_path, sheet_name):
    try:
        # Open the Excel file
        workbook = openpyxl.load_workbook(file_path, read_only=True)

        # Select the specific sheet
        sheet = workbook[sheet_name]

        return workbook, sheet

    except Exception as e:
        print(f"An error occurred while loading the Excel file: {str(e)}")
        return None, None

# Function to count even rows until an empty cell is encountered
def count_even_rows(sheet, column_letter, start_row):
    even_row_count = 0
    row = start_row
    
    while True:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            break
        if row % 2 == 0:
            even_row_count += 1
        row += 2
    
    return even_row_count

# Function to enter data into a web page
def enter_data(data):
    time.sleep(1)
    for _ in range(6):
        pyautogui.press('tab')
    
    # Loop through the data and enter it
    for value in data:
        pyautogui.write(str(value))
        pyautogui.press('tab')
    
    # Handle tickboxes
def tick_box (tickbox):
    for value in tickbox:
        if value == 'Yes':
            pyautogui.press('space')
        pyautogui.press('tab')
    pyautogui.press('enter')

# wait for logo to load then continue
def find_logo():
    time.sleep(1)
    image = pyautogui.locateOnScreen("TARSautomation\\img\\accor_logo.PNG", confidence=0.8)
    time.sleep(1)
    while image == None:
        image = pyautogui.locateOnScreen("TARSautomation\\img\\accor_logo.PNG", confidence=0.8)
        print("still haven't found the image")
    print("Page loaded successfully!!")
    time.sleep(1)

# function for input description into translation page
def enter_description(keys):
    find_logo()
    pyautogui.click(x=971, y=343)  # Click on name search bar
    pyautogui.typewrite(f'{keys}')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=169, y=393)
    find_logo()
    pyautogui.click(x=75, y=355)
    time.sleep(2)
    pyautogui.click(x=388, y=864)
    time.sleep(1)
    pyautogui.typewrite(description[f'{keys}'], interval=0.01)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.click(x=1027, y=599)
    time.sleep(2)
    pyautogui.click(x=52, y=738)
    find_logo()

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Open web browser and navigate to a page
webbrowser.open('https://dataweb.accor.net/dotw-trans/displayHotelLounges!input.action')
find_logo()
pyautogui.click(x=70, y=229)

# Navigate to Lounges library tab
for _ in range(2):
    pyautogui.press('tab')

time.sleep(1)
pyautogui.press('enter')
pyautogui.click(x=148, y=342)
pyautogui.typewrite("MEET")
pyautogui.press('enter')

time.sleep(1)
pyautogui.click(x=1642, y=396)

# Load workbook and read the data
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Meeting Room"  
description = {}
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Count even rows
        even_row_count = count_even_rows(sheet, "C", 12)
        print("Count of even rows until an empty cell:", even_row_count)

        # Loop through the rows and enter data
        cell_start = 12
        for i in range(even_row_count):
            data = [sheet[f"C{cell_start}"].value,
                    sheet[f"G{cell_start}"].value,
                    sheet[f"F{cell_start}"].value,
                    sheet[f"H{cell_start}"].value,
                    sheet[f"I{cell_start}"].value,
                    sheet[f"L{cell_start}"].value,
                    sheet[f"N{cell_start}"].value,
                    sheet[f"J{cell_start}"].value,
                    sheet[f"M{cell_start}"].value,
                    sheet[f"K{cell_start}"].value,
                    sheet[f"O{cell_start}"].value,
                    sheet[f"Q{cell_start}"].value,
                    sheet[f"P{cell_start}"].value,
                    sheet[f"R{cell_start}"].value]
            tickbox = [sheet[f"S{cell_start}"].value,
                       sheet[f"T{cell_start}"].value,
                       sheet[f"U{cell_start}"].value,
                       sheet[f"V{cell_start}"].value]
            description[sheet[f"C{cell_start}"].value] = (sheet[f"E{cell_start + 1}"].value)
            
            # Enter data into the web page
            enter_data(data)
            tick_box(tickbox)
            
            time.sleep(2)
            pyautogui.click(x=236, y=340)
            time.sleep(1)
            pyautogui.click(x=1642, y=396)
            
            cell_start += 2

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

# Go to the first page

pyautogui.click(x=96, y=269)

print('Add meeting room successfully!!')
print('Next add translation. . .')

for key in description:
    enter_description(key)
    
print('Task meeting Room Done! --> Next Add Mean of Access')

