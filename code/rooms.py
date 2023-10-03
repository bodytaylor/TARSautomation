import time
import pyautogui
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# set file path and url
url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Roomtypes"

# open url and load excel file
open_web(url)          
load_excel_file(excel_file_path, sheet_name)

# import room data for seach in the menu

excel_file = 'TARSautomation\\room_library.xlsx'
room_df = pd.read_excel(excel_file)

# function for finding room category
def get_category_by_code(df, code):
    matching_categories = df[df['code'] == code]['category'].tolist()
    return matching_categories

try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        
        # loop until room code is none
        cell_start = 11
        i = 0
        while True:
            # locate a menu and search for room type
            room_code = str(sheet[f'C{cell_start + i}'].value)
            if room_code != 'None':
                # Check Room Code
                category = get_category_by_code(room_df, code=room_code)[0]
                product_search(product_type=category, text_search=room_code)
                print(category)
                find_add()
                time.sleep(2)
                # Add data
                # tick on site or close by -> Room always onsite 7 times to this section
                find_and_click_on('TARSautomation\\img\\add_product.PNG')
                tabing(4)
                
                # paying product tickbox
                pyautogui.press('space')
                tabing(1)
                
                # book abble product tickbox
                pyautogui.press('space')
                tabing(1)           
                 
                # Web only tickbox = skip this one 
                tabing(1)
                
                # Max Occupency 
                max_occ = str(sheet[f'S{cell_start + i}'].value)
                pyautogui.write(max_occ)
                tabing(1)
                
                # Adult
                adult = str(sheet[f'T{cell_start + i}'].value)
                pyautogui.write(adult)
                tabing(1)
                
                # Children
                children = str(sheet[f'U{cell_start + i}'].value)
                pyautogui.write(children)
                tabing(1)
                
                # Nb of beds for 1 pax
                bed_for_1 = str(sheet[f'L{cell_start + i}'].value)
                pyautogui.write(bed_for_1)
                tabing(1)          
                
                # Nb of beds for 2 pax
                bed_for_2 = str(sheet[f'M{cell_start + i}'].value)
                pyautogui.write(bed_for_2)
                tabing(1)       
                    
                # room size
                room_size = str(sheet[f'Q{cell_start + i}'].value)
                pyautogui.write(room_size)
                tabing(2) 
                
                # Quantity of product
                quantity = str(sheet[f'V{cell_start + i}'].value)
                pyautogui.write(quantity)
                tabing(1) 
                
                # PMS product code -> Put room code
                pyautogui.write(room_code)
                tabing(1)
                
                # Available on GDS and Media (always tick)
                pyautogui.press('space')
                tabing(1)
                
                # Order in RESA Screen 
                order_resa = str(sheet[f'K{cell_start + i}'].value)
                pyautogui.write(order_resa)
                tabing(1)
                
                # Max quantity of the product in room -> skip
                tabing(1)
                
                # Click add
                pyautogui.press('enter')
                time.sleep(2)
                
                # Print the result
                print(f'{room_code} was added successfully!')
                
                i += 1
            else:
                break
                
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

print('All Rooms was added to TARS!')
print('Next Step Room discription and translation')