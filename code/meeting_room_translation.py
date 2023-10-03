import time
import pyautogui
import webbrowser
import openpyxl
import pandas as pd
from functions import *

# search for non accepted charecters in data frame
def check_text_meet(df, col,):
    df['Non_Matching_Chars'] = df[col].apply(find_non_matching_chars)
    accept = 0
    for index, row in df.iterrows():
        non_matching_chars = row['Non_Matching_Chars']
        if non_matching_chars:
            print(f"Row {df.iloc[index, 0]} column {col}: Detected characters: '{non_matching_chars}'")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()

# Check Description lengh
def check_descrip_len(df, col):
    accept = 0
    for index, description in df.iterrows():
        if len(description) > 255:
            print(f"Row {df.iloc[index, 0]} column {col}: contain more than 255 charactors")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()

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
    
# find and click on add item
def find_add():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('TARSautomation\\img\\add.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()

# wait for logo to load then continue
def find_logo():
    time.sleep(1)
    image = pyautogui.locateOnScreen("TARSautomation\\img\\accor_logo.PNG", confidence=0.8)
    time.sleep(1)
    while image == None:
        image = pyautogui.locateOnScreen("TARSautomation\\img\\accor_logo.PNG", confidence=0.8)
        print("Page is loading . .")
        time.sleep(1)
    print("Page loaded successfully!!")
    time.sleep(1)
    
# find search box
def find_searchbox():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('TARSautomation\\img\\filter.PNG', confidence=0.8)
    pyautogui.moveTo(x, y + 30, 0.1)
    pyautogui.click()

# function for input description into translation page
def enter_description(keys, search_key):
    # Open new tab and locate menu
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelLoungeInput.action?actionType=translate&description.lounge.type.code=MEET&description.lounge.name={search_key}&'
    webbrowser.open_new_tab(url)
    find_logo()
    find_and_click('TARSautomation\\img\\translate.png')
    time.sleep(1)
    find_and_click_on('TARSautomation\\img\\translate_menu.png')
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
    x, y = pyautogui.locateCenterOnScreen('TARSautomation\\img\\add.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()
    
# clear a search box before enter a new search    
def clear_search_box(n):
    for _ in range(n):
        pyautogui.press('del')
        
# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

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
            description[sheet[f"C{cell_start}"].value] = (sheet[f"E{cell_start + 1}"].value)
            cell_start += 2

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

# Create df
df = pd.DataFrame(list(description.items()), columns=['meet_room', 'description'])

# Check Discription before entering it
check_text_meet(df=df, col='description')
check_descrip_len(df=df, col='description')

# If all pass, Add translation
for key in description:
    search_key = str(key).replace(' ', '+')
    enter_description(keys=key, search_key=search_key)
    print(f'Description for {key} has been added')
    
print(f'Translation Added to all meeting rooms in {hotel_rid}')

