import time
import pyautogui
import webbrowser
import openpyxl
import pandas as pd
from functions import *

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

# Function to enter data into a web page
def enter_data(data):
    time.sleep(1)
    for _ in range(6):
        pyautogui.press('tab')
    
    # Loop through the data and enter it
    for value in data:
        if value == None:
            pyautogui.write('0')
            pyautogui.press('tab')
        else:
            pyautogui.write(str(value))
            pyautogui.press('tab')
    
    # Handle tickboxes
def tick_box (tickbox):
    for value in tickbox:
        if value == 'Yes':
            pyautogui.press('space')
        pyautogui.press('tab')
    pyautogui.press('enter')
    
# find and click on add item
def find_add():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\add.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()


# wait for logo to load then continue
def find_logo():
    time.sleep(1)
    image = pyautogui.locateOnScreen("img\\accor_logo.PNG", confidence=0.8)
    time.sleep(1)
    while image == None:
        image = pyautogui.locateOnScreen("img\\accor_logo.PNG", confidence=0.8)
        print("still haven't found the image")
    print("Page loaded successfully!!")
    time.sleep(1)
    
# find search box
def find_searchbox():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\filter.PNG', confidence=0.8)
    pyautogui.moveTo(x, y + 30, 0.1)
    pyautogui.click()

# function for input description into translation page
def enter_description(keys):
    # Open new tab and locate menu
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelLoungeInput.action?actionType=translate&description.lounge.type.code=MEET&description.lounge.name={keys}&'
    webbrowser.open_new_tab(url)
    find_logo()
    find_and_click('img\\translate.png')
    time.sleep(1)
    find_and_click_on('img\\translate_menu.png')
    tabing(5)
    
    # Enter Translations
    pyautogui.typewrite(description[f'{keys}'], interval=0.01)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    
    # go to translate button
    pyautogui.press('enter')
    time.sleep(2)
    # confrim box
    pyautogui.press('enter')
    time.sleep(1)
    # Close tab
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    
        
# find and click on add item
def find_add():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\add.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()
    
# clear a search box before enter a new search    
def clear_search_box(n):
    for _ in range(n):
        pyautogui.press('del')
        
# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Open web browser and navigate to a page
webbrowser.open('https://dataweb.accor.net/dotw-trans/displayHotelLounges!input.action')

# Navigate to Lounges library tab
def locate_menu():
    find_logo()
    pyautogui.click(x=70, y=229)
    
    for _ in range(2):
        pyautogui.press('tab')

    time.sleep(1)
    pyautogui.press('enter')
    pyautogui.click(x=148, y=342)
    clear_search_box(4)
    pyautogui.typewrite("MEET")
    pyautogui.press('enter')
    find_add()
    time.sleep(1)


# Load workbook and read the data
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
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
            data = [
                    str(sheet[f"C{cell_start}"].value).strip(),
                    int(round((sheet[f"G{cell_start}"].value), 0)),
                    sheet[f"F{cell_start}"].value,
                    round((sheet[f"H{cell_start}"].value), 2),
                    sheet[f"I{cell_start}"].value,
                    sheet[f"L{cell_start}"].value,
                    sheet[f"N{cell_start}"].value,
                    sheet[f"J{cell_start}"].value,
                    sheet[f"M{cell_start}"].value,
                    sheet[f"K{cell_start}"].value,
                    sheet[f"O{cell_start}"].value,
                    sheet[f"Q{cell_start}"].value,
                    sheet[f"P{cell_start}"].value,
                    sheet[f"R{cell_start}"].value
                    ]
            tickbox = [sheet[f"S{cell_start}"].value,
                       sheet[f"T{cell_start}"].value,
                       sheet[f"U{cell_start}"].value,
                       sheet[f"V{cell_start}"].value]
            description[sheet[f"C{cell_start}"].value] = (sheet[f"E{cell_start + 1}"].value)
            
            locate_menu()
            
            # Enter data into the web page
            enter_data(data)
            tick_box(tickbox)
            print(f"{sheet[f'C{cell_start}'].value} has been added to Lounges!")
            cell_start += 2

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

# instruction for next step
print('Add meeting room successfully!!')
print('Next add translation. . .')


