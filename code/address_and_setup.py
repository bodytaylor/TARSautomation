import time
import pyautogui
import webbrowser
import openpyxl
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Open web browser and navigate to a page
webbrowser.open('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')
find_logo()

# Navigate to content input tab
find_and_click_on('TARSautomation\\img\\address.PNG')
tabing(3)

# Load workbook and read the data
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Address&Setup"  
description = {}

try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        data = sheet[f"C"].value,


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

