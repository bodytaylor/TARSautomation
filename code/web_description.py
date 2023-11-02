import pandas as pd
from openpyxl import load_workbook
import time
from functions import *

def enter_description(keys, search_key):
    # Open new tab and locate menu
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelLoungeInput.action?actionType=translate&description.lounge.type.code=MEET&description.lounge.name={search_key}'
    webbrowser.open_new_tab(url)
    find_logo()
    find_and_click('img\\translate.png')
    time.sleep(1)
    find_and_click_on('img\\translate_menu.png')
    tabing(5)
    
# Enter Translations
def product_description(code, type, description, marketing):
    
    # Open Web Browser on translate page and wait for webpage load
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={code}&hotelProduct.type.code={type}&hotelProduct.centralUse=true&'
    open_web(url)
    find_logo()
    
    # Click on Translate 
    find_and_click('img\\translate.png')
    time.sleep(2)
    
    # Click on menu and locate discription input box
    find_and_click_on('img\\translate_product.PNG')
    tabing(6)
         
    # Get data from DataFrame and type in the discription box, do not change the secound locater!
    if description != None:
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('del')
        type_translate(2, description)
    else:
        tabing(2)

    # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
    if marketing != None:   
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('del')
        type_translate(1, marketing)
    else:
        tabing(1)

    # Click Translate!
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')

    # close browser
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'w')    


# read description
def extract_data_from_excel(file_path):
    data_list = []

    # Load the Excel file
    wb = load_workbook(file_path, data_only=True)
    ws = wb['Main services']  # Specify the sheet name here

    # Initialize row and column indices
    current_row = 40
    current_col = 3  # Column C

    while current_row <= 125:
        l_value = ws.cell(row=current_row, column=12).value  # Column L

        if l_value == "Yes":
            code = str(ws.cell(row=current_row, column=current_col).value)[0:6].strip()
            description = None
            marketing = None

            # Check the next row for Description or Marketing
            for i in range(1, 3):
                cell_value = str(ws.cell(row=current_row + 1, column=current_col).value).split()
                
                if "Description." in cell_value:
                    description = ws.cell(row=current_row + 1, column=4).value
                elif "Marketing" in cell_value:
                    marketing = ws.cell(row=current_row + 1, column=4).value

            # Append the data to the list of dictionaries
            data_list.append({'Code': code, 'Description': description, 'Marketing': marketing})

        current_row += 1

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_list)

    return df

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        element = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return element
    else:
        return None

# find type of product
def find_type(df, code):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        return result[2]
    else:
        return None

def add(hotel_rid):
    print("[WARNING] - Please Check Loading Form and Clean up all note from the code section!")
    print("[WARNING] - V.10 DWBUS -> DWBUS1")
    print("[WARNING] - V.10 DWCCL1 -> DWCCL")
    
    continue_program()
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    df = extract_data_from_excel(file_path)

    # open web
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(2)

    # Let's rolls!
    for index, row in df.iterrows():
        code = row['Code']
        product_to_add = add_product(code, df=product_lib_df)
        type_and_enter(product_to_add)
        time.sleep(1)
        
        # always yes on GDS
        tick_box(element='hotelProduct.availableOnGDSMedia')
            
        # Click add
        type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
        print(f'INFO - {code} has been added')
        time.sleep(1.5)  
        
    # Add description
    for index, row in df.iterrows():
        code = row['Code']
        type = find_type(code=code, df=product_lib_df)
        des = row['Description']
        mk_label = row['Marketing']
        product_description(code=code, description=des, marketing=mk_label, type=type)
        print(f'INFO - Desciption for {code} has been added')
    
