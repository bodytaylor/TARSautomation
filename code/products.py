import time
import pyautogui
import pandas as pd
from functions import *

# version 1.0.2
# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# set file path and url
url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Other Services"

# open url and load excel file
open_web(url)      
load_excel_file(excel_file_path, sheet_name)

# import room data for seach in the menu
excel_file = 'product_library.xlsx'
product_df = pd.read_excel(excel_file)

# function for finding room category
def get_category_by_code(df, code):
    matching_categories = df[df['code'] == code]['category'].tolist()
    return matching_categories

# Locate add product menu
def locate_product_menu():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\product.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    tabing(3)
    pyautogui.press('enter')

# Search in dropdown list
def product_search(product_type):
    x, y = pyautogui.locateCenterOnScreen('img\\dropdown.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    pyautogui.press('(')
    time.sleep(3)
    loop_key_press(product_type)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    
# Search for product code
def code_search(text_search):
    find_searchbox()
    clear_search_box(6)
    pyautogui.write(text_search)
    pyautogui.press('enter')

try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        
        # loop until room code is none
        cell_start = 11
        i = 0
        
        if i == 0:
            previous_search = ''
        
        code_not_found = []
        
        while True:
            product_code = str(sheet[f'C{cell_start + i}'].value).strip()  
            product_available = str(sheet[f'I{cell_start + i}'].value)  
            paying = str(sheet[f'J{cell_start + i}'].value) 
            
            # If Yes fill the data       
            if product_available == 'Yes':
                # compare product code in the index book
                if len(get_category_by_code(product_df, code=product_code)) != 0:
                    category = get_category_by_code(product_df, code=product_code)[0]
                    
                    # locate a menu and search for product type
                    locate_product_menu()
                    # skip first round
                    # skip product search if previous search = current search

                    if category != previous_search:
                        product_search(product_type=category)
                        
                    code_search(product_code)    
                    find_add()      
                    time.sleep(2)                                   
                    find_and_click_on('img\\add_product.PNG')
                    tabing(4)

                    # Check if it paying ?
                    if paying == 'Yes':
                        pyautogui.press('space')
                    tabing(3)
                    
                    # Occupancy = 1
                    if paying == 'Yes':
                        pyautogui.write('1')
                    tabing(5)
                            
                    # always tick on available on GDS
                    pyautogui.press('space')
                    tabing(2)
                    
                    # Max quantity of product in room = 1
                    if paying == 'Yes':
                        pyautogui.write('1')
                    tabing(1)
                            
                    # go to add button
                    pyautogui.press('enter')
                    
                    # update search
                    previous_search = category
                    
                else:
                    code_not_found.append(product_code)
            
            i += 1
            if product_code == 'None':
                break
                        
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()
        
print(f'Please manually check {code_not_found}')