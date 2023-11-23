import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *

# execute java script
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')

# Tickbox in browser console
def tick_box(element):
    script = (f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
    return script

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
    # Do not add this code
    meal_options_list = ['MBREAK', 'MBUFF', 'DMBREA', 'AMBREA']
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

    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    # open web
    driver.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(1)
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="classicTabName"]'))
        )
    print(f'[INFO] - {page.text}')
    
    product_not_found = []
    error = []
    for index, row in df.iterrows():
        code = row['code']
        if code not in meal_options_list:
            product_to_add = add_product(code, df=product_lib_df)
            if product_to_add is None:
                product_not_found.append(code)
            else:
                driver.execute_script(product_to_add)
                
                # Wait for page to load
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                    )

                amount = row['amount']
                if pd.isna(amount) == False:
                    amount = str(int(row['amount']))
                    input_text(element_id='hotelProduct.quantity', text=amount)
                
                # always yes on GDS
                driver.execute_script(tick_box(element='hotelProduct.availableOnGDSMedia'))
                
                # Click add
                driver.execute_script('document.getElementById("hotelProduct.submitButton").click();')
                
                # Wait for response
                get_response(driver=driver, code=code, error=error)

    # Print result to user
    print(f'Main Product has been added to {hotel_rid}!')
    if len(product_not_found) != 0:
        print(f'[INFO] - Product not found {product_not_found}')
    if len(error) != 0:
        print('##### Mission Report #####')
        for i in error:
            print(i)
