import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from functions import *

# get room code and store as list
def get_room_data(hotel_rid):
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Roomtypes"
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols='C, AC, AA', skiprows=9, nrows=300)
    df.columns = ['room_code', 'marketing_label', 'tar_ref']
    df = df.dropna()
    df = df.reset_index(drop=True)
    print(df)
    # in case of error
    # df = df.drop(df.index[0:7])
    return df

# find type of product
def find_type(df, code):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        return result[2]
    else:
        return None

def add(hotel_rid):
    translate_or_update = int(input('Translate Hit: 1 \nUpdate Hit: 2\nPlease type number and Hit Enter: '))
    # Get room data from excel sheet
    
    # Check for unaccepted characters, if there are any, script will terminate!
    while True:
        df = get_room_data(hotel_rid)
        marketing_check = check_text(df, col='marketing_label')
        tar_ref_check = check_text(df, col='tar_ref')
        if marketing_check == tar_ref_check == 0:
            break
        continue_program()
        
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )
    
    # import driver session
    from  web_driver_init import driver
    
    # error
    error = []
    
    # Start the loop!
    for i in range(len(df)):
        # Get room code
        room_code = df.iloc[i, 0]
        room_type = find_type(df=product_lib_df, code=room_code)
        
        # Open Web Browser on translate page and wait for webpage load
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={room_code}&hotelProduct.type.code={room_type}&hotelProduct.centralUse=true&'
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "zoneCliquable"))
            )
        
        # Click on Translate 
        driver.execute_script(f"displayTranslateForm('translateInput','GB','{room_code}','{room_type}','{hotel_rid}','productsDescriptionsTable','true','true','GB','true')")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="translateHotelProductFormJson"]'))
            )
        
        # find description box
        description_box = driver.find_element(By.ID, "hotelProductTranslate.description")
        marketing_box =  driver.find_element(By.ID, "hotelProductTranslate.referenceLabel")
        
        # Clear the box if update option is on
        if translate_or_update == 2:
            marketing_box.clear()
            description_box.clear() 
            
        # Get data from DataFrame and type in the discription box, do not change the secound locater!
        description = df.iloc[i, 2]
        description_box.send_keys(description)
            
        # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
        marketing_label = df.iloc[i, 1]
        marketing_box.send_keys(marketing_label)

        # Select translate or update
        if translate_or_update == 1:
            # Click on Translate button
            script = """
            document.getElementById('translateHotelProductForm.submitButton').click();
            """
            
            driver.execute_script(script)
            time.sleep(1)
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(1)
        else:
            script = """
            document.getElementById('translateHotelProductForm.submitSaveButton').click();
            """

            driver.execute_script(script)
            time.sleep(1)
            
        # get response
        get_response(driver=driver, code=room_code, error=error)

    if translate_or_update == 1:
        print(f'Translation for all rooms in {hotel_rid} is done!')
    else:
        print(f'Discription for all rooms in {hotel_rid} is done! Please comeback and hit translate later!')
        
    # Print error to user
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')