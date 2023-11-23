import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *

def tick_box(element):
    driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
    time.sleep(0.1)

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        script = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return script
    else:
        return None
    
# Load Room Data
def load_room_data(hotel_rid):
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Roomtypes"
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=8, dtype=str)
    df = df.dropna(subset=['TARS product code'])
    df = df.dropna(axis=1, how='all')
    df = df.drop(columns=['Unnamed: 1'])
    df = df.reset_index(drop=True)
    df = df.drop(index=0)
    columns_to_drop = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(columns=columns_to_drop)
    # to remove in case of error use this line below replace with row number to start
    # df = df.drop(df.index[0:13])
    return df

def add(hotel_rid):
    # set file path and url
    url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'

    # open url and load excel file
    driver.get(url) 
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="classicTabName"]'))
        )
    print(f'[INFO] - {page.text}') 
    
    # Error collector
    code_error = []
    product_error = []        

    try:
        # Load Excel file and select the sheet
        room_data = load_room_data(hotel_rid)
        print(room_data)
        
        # Load product library
        csv_path = 'products_lib.csv'
        product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
        )
        
        
        
        # loop until room code is none
        # Default Value is 11
        for index, row in room_data.iterrows():
            # locate a menu and search for room type
            room_code = str(row['TARS product code']).strip()
            # Check Room Code
            add = (add_product(code=room_code, df=product_lib_df))
            if add is not None:
                driver.execute_script(add)
                
                # waiting for input form
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                    )  
                
                # paying product tickbox
                tick_box('hotelProduct.paying')
                    
                # book abble product tickbox
                tick_box('hotelProduct.bookable')        
                        
                # Max Occupency 
                max_occ = str(row['Maximum occupancy *']).strip()
                input_text(element_id='hotelProduct.maxOccupancyTotal', text=max_occ)
                        
                # Adult
                adult = str(row['Maximum adults *']).strip()
                input_text(element_id='hotelProduct.maxOccupancyAdult', text=adult)
                        
                # Children
                children = str(row['Maximum children *']).strip()
                input_text(element_id='hotelProduct.maxOccupancyChildren', text=children)
                        
                # Nb of beds for 1 pax
                bed_for_1 = str(row['Nb of bed available for\n1 pax *']).strip()
                input_text(element_id='hotelProduct.singleBebNumber', text=bed_for_1)      
                        
                # Nb of beds for 2 pax
                bed_for_2 = str(row['Nb of bed available for\n2 pax *']).strip()
                input_text(element_id='hotelProduct.doubleBebNumber', text=bed_for_2)   
                            
                # room size
                room_size = str(row['Room size m²*']).strip()
                input_text(element_id='hotelProduct.roomSizeInSquareMeter', text=room_size)
                        
                # Quantity of product
                quantity = str(row['Quantity\nof product *']).strip()
                input_text(element_id='hotelProduct.quantity', text=quantity)
                        
                # PMS product code -> Put room code
                input_text(element_id='hotelProduct.pmsCode', text=room_code)
                        
                # Available on GDS and Media (always tick)
                tick_box('hotelProduct.availableOnGDSMedia')
                        
                # Order in RESA Screen 
                order_resa = str(row['Order \nin resa \nscreen *'])
                input_text(element_id='hotelProduct.orderInResaScreen', text=order_resa)
                        
                # Max quantity of the product in room -> skip
                        
                # Click add
                driver.execute_script('submitFormProduct();')
                        
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
                    product_error.append(f'{room_code}: {error_message.text}')
                    print(f'[INFO] - {error_message.text}')
                        
            else:
                code_error.append(room_code)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        print('Automation Complete')
        if len(product_error) != 0:
            for i in product_error:
                print(f'[ERROR] - {i}')
        elif len(code_error) != 0:
            print(f'[ERROR] - CODE NOT FOUND IN LIBRARY {code_error}')
            