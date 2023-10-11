import pandas as pd
from functions import *

# Do not add this code
meal_options_list = ['MBREAK', 'MBUFF', 'DMBREA', 'AMBREA']

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')


# Read Excel file and put in data frame
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = 'Main services'
row_start = 11
row_end = 37
cell_add1 = []
cell_add2 = []
cell_add3 = []
for i in range(row_start, row_end + 1):
    cell_add1.append(f'C{i}')
    cell_add2.append(f'J{i}')
    cell_add3.append(f'K{i}')
code = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add1)
available = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add2)
amount = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add3)
df = pd.DataFrame({'code': code, 'available': available, 'amount': amount})

# clean df and filter for available product
df.dropna(subset=['available'], inplace=True)
df = df.loc[df['available'] == 'Yes']

# read product library
excel_file = 'product_library.xlsx'
product_df = pd.read_excel(excel_file)

# open web
url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
open_web(url)

i = 0
for index, row in df.iterrows():
    code = row['code']
    if code not in meal_options_list:
        category = get_category_by_code(product_df, code)[0]
    
        # Check Catagory before search
        locate_product_menu()
        if i == 0:
                previous_search = ''
        if category != previous_search:
            product_search(product_type=category)

        code_search(code)
        find_add()
        time.sleep(2)
        find_and_click_on('img\\add_product.PNG')
        tabing(10)
        
        amount = row['amount']
        if pd.isna(amount) == False:
            amount = str(int(row['amount']))
            pyautogui.typewrite(amount)
        
        tabing(2)
        # tick on available on GDS
        pyautogui.press('space' )
        tabing(3)
        
        pyautogui.press('enter')
        
        previous_search = category
        i += 1
    
print(f'Main Product has been added to {hotel_rid}!')
