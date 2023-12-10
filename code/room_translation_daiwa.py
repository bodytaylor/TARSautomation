import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import *
import pandas as pd
from functions import *
import os
from dotenv import load_dotenv

# Load environment variables from .env file
def user_credential():
    load_dotenv()

    # Access the variables using os.environ.get()
    username = os.environ.get("TARSUSER")
    password = os.environ.get("PASSWORD")

    # Check if .env file exists
    if not (username and password):
        print("No .env file found. Please provide your credentials:")
        username = input("Username: ")
        password = input("Password: ")

        # Save the credentials to a new .env file
        with open(".env", "w") as env_file:
            env_file.write(f"TARSUSER={username}\n")
            env_file.write(f"PASSWORD={password}\n")

        print(".env file created with provided credentials.")
    else:
        print(f"Credentials loaded from .env file. Username: {username}")
        
    return username, password

def login(username, password):
        # Navigate to the login page
    driver.get("https://dataweb.accor.net/dotw-trans/login!input.action")

    # Wait for an element to be visible
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "login"))
        )
            # Find the username and password input fields and enter your credentials
        username_field = driver.find_element(By.ID, "loginField")
        password_field = driver.find_element(By.NAME, "password")


        driver.execute_script("arguments[0].value = '';", username_field)
        username_field.send_keys(username)
        driver.execute_script("arguments[0].value = arguments[1];", password_field, password)

        # Submit the login form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input#login_0[value="Submit"].submit')

        # Click the button
        password_field.send_keys(Keys.RETURN)
    except ValueError as e:
        print(e)

def response():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]/ul/li/span'))
        )
        span_element = element.find_element(By.XPATH, '//*[@id="actionmessage"]/ul/li/span')
        span_text = span_element.text
        return span_text
    except:
        return None
    
def hotel_search(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]'))
        )
        driver.execute_script('document.getElementById("keyword").value = "";')
        element.send_keys(f'{hotel_rid}')
        search_button = driver.find_element(By.ID, 'searchButton')
        count = 0
        
        while True:
            search_button.send_keys(Keys.RETURN)
            action_res = response()
            time.sleep(2)
            count += 1
            
            if action_res is None:
                hotel_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hotelNameClass'))
            )
                hotel_name = driver.find_element(By.CLASS_NAME, 'hotelNameClass')
                text = hotel_name.text
                print(f'Selected Hotel: {text}')
                break
            elif count == 5:
                print('No Hotel Found!')
                break
            
    except ValueError as e:
        print(e)

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

# Get response
def get_response(driver, code, error=list, rid=str):
     # Get response
            WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="messages"]'))
                ) 
            time.sleep(0.5)
            try:
                action_message_element = WebDriverWait(driver, 7).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]'))
                    )
                action_message = action_message_element.find_element(By.TAG_NAME, 'span').text
                print(f'[INFO] - {action_message}')
            except:
                error_message = action_message_element = WebDriverWait(driver, 7).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="errormessage"]'))
                    )
                error.append(f'{rid} - {code}: {error_message.text}')
                print(f'[INFO] - {rid} - {code}: {error_message.text}')
                
    
def loading_form(file_path):
    df = pd.read_excel(file_path, dtype=str)
    return df

def add():
    user, password = user_credential()
    login(user, password)
    
    df = loading_form(r"D:\NSANGKARN\Downloads\Clean DR Description_231130.xlsx")
    translate_or_update = 2
    # Get room data from excel sheet
        
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )
    
    # error
    error = []
    
    # Previous RID
    previous_rid = ''
    
    # Start the loop!
    for index, row in df.iterrows():
        rid = row['RID']
        if rid != previous_rid:
            hotel_search(rid)
            
        # Get room code
        room_code = str(row['Room type Code']).strip()
        room_type = find_type(df=product_lib_df, code=room_code)
        
        # Open Web Browser on translate page and wait for webpage load
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={room_code}&hotelProduct.type.code={room_type}&hotelProduct.centralUse=true&'
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "zoneCliquable"))
            )
        
        # Click on Translate 
        driver.execute_script(f"displayTranslateForm('translateInput','JA','{room_code}','{room_type}','{rid}','productsDescriptionsTable','true','true','JA','true')")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="translateHotelProductFormJson"]'))
            )
        
        # find description box
        marketing_box =  driver.find_element(By.ID, "hotelProductTranslate.referenceLabel")
        
        # Clear the box if update option is on
        driver.execute_script('document.getElementById("hotelProductTranslate.referenceLabel").value = "";')
            
        # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
        marketing_label = row['Japanese Room type translation(New)']
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
        get_response(driver=driver, code=room_code, error=error, rid=rid)
        
        # English Translation
        english_label = row['English Room type Name (New)']
        
        if type(english_label) == str: 
            # Click on Translate 
            driver.execute_script(f"displayTranslateForm('translateInput','GB','{room_code}','{room_type}','{rid}','productsDescriptionsTable','true','true','GB','true')")
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="translateHotelProductFormJson"]'))
                )
            
            # find description box
            marketing_box =  driver.find_element(By.ID, "hotelProductTranslate.referenceLabel")
            
            # Clear the box if update option is on
            driver.execute_script('document.getElementById("hotelProductTranslate.referenceLabel").value = "";')
                
            # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
            english_label = row['English Room type Name (New)']
            marketing_box.send_keys(english_label)

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
                
            get_response(driver=driver, code=room_code, error=error, rid=rid)
            
        # update rid
        previous_rid = rid
            
    # Print error to user
    with open(r'"D:\NSANGKARN\Downloads\DR Description_231130.txt', 'w') as fp:
        for item in error:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')
            
if __name__ == "__main__":
    add()