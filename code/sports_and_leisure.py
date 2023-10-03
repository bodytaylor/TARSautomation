import time
import pyautogui
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# set file path and url
url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Sports&Leisure"

# open url and load excel file
open_web(url)      
load_excel_file(excel_file_path, sheet_name)

# import room data for seach in the menu

excel_file = 'TARSautomation\\product_library.xlsx'
product_df = pd.read_excel(excel_file)

# function for finding room category
def get_category_by_code(df, code):
    matching_categories = df[df['code'] == code]['category'].tolist()
    return matching_categories

try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        
        # loop until room code is none
        cell_start = 14
        i = 0
        code_not_found = []
        
        while True:
            product_code = str(sheet[f'C{cell_start + i}'].value).strip()  
            product_available = str(sheet[f'H{cell_start + i}'].value)  
            paying = str(sheet[f'J{cell_start + i}'].value) 
            on_site = str(sheet[f'I{cell_start + i}'].value) 
            
            # If Yes fill the data       
            if product_available == 'Yes':
                # compare product code in the index book
                if len(get_category_by_code(product_df, code=product_code)) != 0:
                    category = get_category_by_code(product_df, code=product_code)[0]
                    
                    # locate a menu and search for product type
                    product_search(product_type=category, text_search=product_code)
                    find_add()      
                    time.sleep(2)                                   
                    find_and_click_on('TARSautomation\\img\\add_product.PNG')
                    tabing(3)
                    
                    # is product onsite or close by?
                    if on_site == 'No':
                        pyautogui.press('right')
                        
                    tabing(1)
                    
                    # check if it paying ?
                    if paying == 'Yes':
                        pyautogui.press('space')
                    tabing(3)
                    
                    # Occupancy = 1
                    pyautogui.write('1')
                    tabing(5)
                            
                    # always tick on available on GDS
                    pyautogui.press('space')
                    tabing(2)
                    
                    # Max quantity of product in room = 1
                    pyautogui.write('1')
                    tabing(1)
                            
                    # go to add button
                    pyautogui.press('enter')
                    
                else:
                    code_not_found.append(product_code)
            
            i += 1
            if product_code == None:
                break
                        
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()
        
print(f'Please manually check {code_not_found}')