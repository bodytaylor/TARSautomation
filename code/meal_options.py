import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *

def tick_box(element):
    driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
    time.sleep(0.15)

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.15)

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        script = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return script
    else:
        return None

def add(hotel_rid):
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    # mandatory meal option *** Add According to Pricing book Need to Update
    meal_options_list = ['MBUFF']
    
    meal_data = get_excel_values(file_path=f'hotel_workbook\{hotel_rid}\{hotel_rid} Pricing Book.xlsx',
                                 sheet_name='Set-up table',
                                 cell_addresses=['E459',
                                                 'E460',
                                                 'E461',
                                                 'E462',
                                                 'E465',
                                                 'E466',
                                                 'E467',
                                                 'E468',
                                                 'E475']
                                 )
    # Append to meal option list
    mbreak = meal_data[0]
    mphb = meal_data[1]
    mpfb = meal_data[2]
    packai = meal_data[3]
    dmbrea = meal_data[4]
    dmphb = meal_data[5]
    dmpfb = meal_data[6]
    dpacka = meal_data[7]
    mbuff = meal_data[8]
    
    if mbreak is not None:
        meal_options_list.extend(['MBREAK', 'AMBREA'])
    if mphb is not None:
        meal_options_list.extend(['MPHB', 'AMPHB'])
    if mpfb is not None:
        meal_options_list.extend(['MPFB', 'AMPFB'])
    if packai is not None:
        meal_options_list.extend(['PACKAI', 'APACKA'])
    if dmbrea is not None:
        meal_options_list.append('DMBREA')
    if dmphb is not None:
        meal_options_list.append('DMPHB')
    if dmpfb is not None:
        meal_options_list.append('DMPFB')
    if dpacka is not None:
        meal_options_list.append('DPACKA')
    if mbuff is not None:
        meal_options_list.append('MBUFF')  
        
    # Print Data to user
    print('Meal Plan to add to the Hotel')
    print(meal_options_list)

    driver.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="classicTabName"]'))
        )
    print(f'[INFO] - {page.text}')
    
    error = []
    # start Loop!
    for item in meal_options_list:
        add = (add_product(item, df=product_lib_df))
        driver.execute_script(add)
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
            )
        
        # Meal is paying product
        tick_box(element='hotelProduct.paying')
        input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
        input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
        input_text(element_id='hotelProduct.orderInResaScreen', text='99')
        input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')
        tick_box(element='hotelProduct.availableOnGDSMedia')
        driver.execute_script('document.getElementById("hotelProduct.submitButton").click();')
        
        # Wait for response
        WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="messages"]'))
            )
        try:
            action_message_element = driver.find_element(By.XPATH, '//*[@id="actionmessage"]')
            action_message = action_message_element.find_element(By.TAG_NAME, 'span').text
            print(f'[INFO] - {action_message}')
        except:
            error_message = driver.find_element(By.XPATH, '//*[@id="errormessage"]')
            error.append(f'{item}: {error_message.text}')
            print(f'[INFO] - {error_message.text}')
        
    print(f'[INFO] - Mandatory Meal Option has been added to {hotel_rid}!')
    if len(error) != 0:
        print('##### Mission Report #####')
        for i in error:
            print(i)
        