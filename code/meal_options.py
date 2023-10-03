import time
import pyautogui
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# set file path and url
url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Other Services"

# open url
open_web(url)      

# mandatory meal option
meal_options_list = ['MBREAK', 'MBUFF', 'DMBREA', 'AMBREA']

# load product categories
excel_file = 'TARSautomation\\product_library.xlsx'
product_df = pd.read_excel(excel_file)


# start Loop!
for i in range(len(meal_options_list)):
    code = meal_options_list[i] 
    category = get_category_by_code(product_df, code)[0]
    product_search(product_type=category, text_search=code)
    find_add()
    time.sleep(2)
    find_and_click_on('TARSautomation\\img\\add_product.PNG')
    tabing(4)
    
    # always tick paying
    pyautogui.press('space')
    tabing(3)
    
    # Occupancy = 1
    pyautogui.write('1')
    tabing(5)
    
    # Always Tick on Available on GDS and Media
    pyautogui.press('space')
    tabing(2)
    
    # Max quantity of product in room = 1
    pyautogui.write('1')
    tabing(1)
    
    pyautogui.press('enter')
    
print(f'Mandatory Meal Option has been added to {hotel_rid}!')

        
