import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
import pandas as pd
from functions import *


# execute java script
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')

# Tickbox in browser console
def tick_box(element):
    driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')

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
    
    driver.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(1)
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="classicTabName"]'))
        )
    print(f'[INFO] - {page.text}')

    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        if workbook and sheet:
            
            # loop until room code is none
            cell_start = 14
            i = 0
            code_not_found = []
            error = []
            
            while True:
                product_code = str(sheet[f'C{cell_start + i}'].value).strip()  
                product_available = str(sheet[f'H{cell_start + i}'].value)  
                paying = str(sheet[f'J{cell_start + i}'].value) 
                on_site = str(sheet[f'I{cell_start + i}'].value) 
                
                # If Yes fill the data       
                if product_available == 'Yes':
                    product_to_add = add_product(product_code, df=product_lib_df)
                    if product_to_add == None:
                        code_not_found.append(product_code)
                    else:
                        driver.execute_script(product_to_add)
                        # Wait for page to load
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                            )
                        # is product onsite or close by?
                        if on_site == 'No':
                            driver.execute_script('document.getElementById("hotelProduct.onSiteCloseBy0").checked = true;')
                                
                        # check if it paying ?
                        if paying == 'Yes':
                            tick_box(element='hotelProduct.paying')
                            input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
                            input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
                            input_text(element_id='hotelProduct.orderInResaScreen', text='99')
                            input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')

                        # always tick on available on GDS
                        tick_box(element='hotelProduct.availableOnGDSMedia')
                        
                        # Click Add
                        driver.execute_script('document.getElementById("hotelProduct.submitButton").click();')
                        
                        # Wait for response
                        get_response(driver=driver, code=product_code, error=error)
 
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
    if len(error) != 0:
        for i in error:
            print(i)
            