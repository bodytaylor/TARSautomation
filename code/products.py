import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
import pandas as pd
from functions import *

# version 1.0.2

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
    # set file path and url
    url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Other Services"

    # Load excel file to Pandas Data Frame
    products_df = pd.read_excel(excel_file_path, sheet_name=sheet_name, skiprows=9)

    # Clean data
    products_df = products_df.drop(columns=['Unnamed: 0', 'Family', 'Hotel services', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
                            'Displayed on AccorHotels.com', 'Amount', 'Unnamed: 11'])
    products_df = products_df.dropna()
    products_df = products_df[products_df['Product is present\nYes/No'] != 'No']
    products_df = products_df.rename(columns={
        'Product is present\nYes/No': 'available',
        'Paying\nYes/No': 'paying'
    })

    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    driver.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(1)
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="classicTabName"]'))
        )
    print(f'[INFO] - {page.text}')

    # Start Loop
    products_not_found = []
    error = []
    for index, row in products_df.iterrows():
        code = row['Code']
        add = (add_product(code, df=product_lib_df))
        if add == None:
            products_not_found.append(code)
        else:
            driver.execute_script(add)
            # Wait for page to load
            WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
            )
            
            if row['paying'] == 'Yes':
                driver.execute_script(tick_box(element='hotelProduct.paying'))
                input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
                input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
                input_text(element_id='hotelProduct.orderInResaScreen', text='99')
                input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')
                
            driver.execute_script(tick_box(element='hotelProduct.availableOnGDSMedia'))
            driver.execute_script('document.getElementById("hotelProduct.submitButton").click();')
            
            # Wait for response
            get_response(driver=driver, code=code, error=error)
        
    if len(products_not_found) != 0:
        print(f'[INFO] - Please Manually Check this product: {products_not_found}')
    if len(error) != 0:
        print('##### Mission Report #####')
        for i in error:
            print(i)
        
    