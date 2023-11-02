import time
import pyautogui
import pandas as pd
from functions import *

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        element = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return element
    else:
        return None

def add(hotel_rid):
    # set file path and url
    url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Sports&Leisure"

    # import room data for seach in the menu
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    # open url and load excel file 
    load_excel_file(excel_file_path, sheet_name)
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(2)

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
                    product_to_add = add_product(product_code, df=product_lib_df)
                    type_and_enter(product_to_add)
                    time.sleep(1)
                    # is product onsite or close by?
                    if on_site == 'No':
                        type_and_enter(text='document.getElementById("hotelProduct.onSiteCloseBy0").checked = true;')
                            
                    # check if it paying ?
                    if paying == 'Yes':
                        tick_box(element='hotelProduct.paying')
                        input_textf(element_id='hotelProduct.maxOccupancyTotal', text='1')
                        input_textf(element_id='hotelProduct.maxQtyInRoom', text='1')
                        input_textf(element_id='hotelProduct.orderInResaScreen', text='99')
                        input_textf(element_id='hotelProduct.maxOccupancyAdult', text='1')

                    # always tick on available on GDS
                    tick_box(element='hotelProduct.availableOnGDSMedia')

                    type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
                    print(f'INFO - {product_code} has been added')
                    time.sleep(1.5)
                        
                i += 1  
                if product_code == 'None':
                    break
                            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close()
    
    if len(code_not_found) != 0:
        print(f'[INFOR] - Please Manually Check this product: {code_not_found}')
            