from functions import *
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import pandas as pd
import time

def driver_init():
    # Setup Chrome Driver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_data(element_id=str):
    try:
        element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f'{element_id}'))
        )
        data = element.get_attribute("value")
        print(f"{element_id}: {data}")
        return data
    except ValueError as e:
        print(e)
        
def wait(element_id):
    try:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f'{element_id}'))
        )

    except ValueError as e:
        print(e)
    
        
def input_data(element_id, text):
    try:
        element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f'{element_id}'))
        )
        element.clear()
        element.send_keys(text)

    except ValueError as e:
        print(e)
        
def user_credential():
    load_dotenv()

    # Access the variables using os.environ.get()
    username = os.environ.get("ESMUSER")
    password = os.environ.get("ESMPASSWORD")

    # Check if .env file exists
    if not (username and password):
        print("No .env file found. Please provide your credentials:")
        username = input("ESM Username: ")
        password = input("ESM Password: ")

        # Save the credentials to a new .env file
        with open(".env", "w") as env_file:
            env_file.write(f"ESMUSER={username}\n")
            env_file.write(f"ESMPASSWORD={password}\n")

        print(".env file created with provided credentials.")
    else:
        print(f"Credentials loaded from .env file. Username: {username}")
        
    return username, password

def login(username, password):
        # Navigate to the login page
    driver.get("https://www.esmaccor.com/login")
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'pageloading-mask')))
    
    # Wait for an element to be visible
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
            # Find the username and password input fields and enter your credentials
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Click the button
        password_field.send_keys(Keys.RETURN)
        
    except ValueError as e:
        print(e)
        
def check_esm_user(hotel_rid):
    driver.get('https://www.esmaccor.com/administration/usersearchlist/init')
    # Wait for page to load
    while True:
        wait = WebDriverWait(driver, 10)
        element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
        )
        value = element.get_attribute('data-page-initialized')
        time.sleep(1)
        if value == 'true':
            break
    try:
        hotel_code_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "codeHotel"))
        )

        hotel_code_field.send_keys(hotel_rid)
        time.sleep(1)
        # Search
        hotel_code_field.send_keys(Keys.RETURN)
        
    except ValueError as e:
        print(e)
        
    finally:
        try:
            response = WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/div[2]/fieldset/div/div/div[2]/table/tbody"))
                )
            response_list = []
            for td in response.find_elements(By.TAG_NAME, "td"):
                response_list.append(td.text)
            text = ' '.join(map(str, response_list))  
            emails = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-zA-Z]+", text)   
            print(emails)
            return ','.join(map(str, emails))
            
        except:
            error = WebDriverWait(driver, 7).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "sucessMessage"))
            )   
            print(error.text)
            return error.text
             
def load_esm_form():
    file_path = input('Please specify ESM request form path: ').replace('"', '')
    df = pd.read_excel(file_path, dtype=str)
    return df
   
def write_response(df, hotel_rid, response):
    rid = str(hotel_rid)
    df.loc[df['RID'] == rid, 'ems_check'] = response
    
def print_screen(hotel_rid):
    file_path = f'esm\{hotel_rid}_esm_create.png'
    driver.save_screenshot(file_path)
    
# create account
def create_account(df):
    for index, row in df.iterrows():
        driver.get('https://www.esmaccor.com/en/administration/managercreationmulti/init')
        # Wait for page to load
        while True:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            value = element.get_attribute('data-page-initialized')
            time.sleep(1)
            if value == 'true':
                break
        
        manager_name = row['Last Name']
        manager_first_name = row['First Name']
        manager_email = row['EMAIL 1']
        rid = row['RID']
        input_data(element_id='managerName', text=manager_name)
        input_data(element_id='managerFirstname', text=manager_first_name)
        input_data(element_id='managerMail', text=manager_email)
        input_data(element_id='managerCodeHotel', text=rid)
        
        # click add
        driver.execute_script('document.getElementById("managerAddHotelButton").click();')
        try:
            WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="rowPerPageZone_userGrid"]/table[2]'))
            )
        except ValueError as e:
            print(e)
        time.sleep(1)
        # Wait for page to load
        while True:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            value = element.get_attribute('data-page-initialized')
            time.sleep(1)
            if value == 'true':
                break
        
        # click create
        driver.execute_script('document.getElementById("managerCreationButton").click();')
        # Wait for page to load
        while True:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            value = element.get_attribute('data-page-initialized')
            time.sleep(1)
            if value == 'true':
                break
        try:
            WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'finfo'))
            )
        except:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger'))
            )
            # extract user from server response
            pattern = r'used by (\w+)'
            response = element.text
            match = re.search(pattern, response)
            username = match.group(1)
            add_hotel_to_user(username, rid)
            
def add_hotel_to_user(username, hotel_rid):
    driver.get('https://www.esmaccor.com/en/administration/managersearchmulti')
    while True:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            value = element.get_attribute('data-page-initialized')
            time.sleep(1)
            if value == 'true':
                break
            
    input_data(element_id='managerLogin', text=username)

    # search
    driver.execute_script('document.getElementById("searchButton").click();')
    time.sleep(2)
    wait_page_load()
    input_data(element_id='managerCodeHotel', text=hotel_rid)
    driver.execute_script('document.getElementById("managerAddHotel").click();')
    time.sleep(2)
    wait_page_load()
    driver.execute_script('document.getElementById("updateHotel").click();')
    time.sleep(2)
    
def wait_page_load():
    while True:
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
        value = element.get_attribute('data-page-initialized')
        time.sleep(1)
        if value == 'true':
            break
        
def delete_esm(df):
    for index, row in df.iterrows():
        driver.get('https://www.esmaccor.com/en/administration/userdeleted')
        # Wait for page to load
        while True:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            value = element.get_attribute('data-page-initialized')
            time.sleep(1)
            if value == 'true':
                break
            
        rid = row['RID']
        input_data(element_id='codeHotel', text=rid)
        driver.execute_script('document.getElementById("deleteButton").click();')
        time.sleep(3)
        
def get_screenshot(df):
    # add new column
    df['user'] = ''
    df['esm_email'] = ''
    df['result'] = ''
            
    for index, row in df.iterrows():
        driver.get('https://www.esmaccor.com/en/administration/usersearchlist/init')
        # Wait for page to load
        wait_page_load()
            
        rid = row['RID']
        input_data(element_id='codeHotel', text=rid)
        driver.execute_script('document.getElementById("managerCreationButton").click();')
        
        try:
            response = WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/div[2]/fieldset/div/div/div[2]/table/tbody"))
                )
            response_list = []
            for td in response.find_elements(By.TAG_NAME, "td"):
                response_list.append(td.text)
            text = ' '.join(map(str, response_list))  
            user = response_list[0]
            email = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-zA-Z]+", text) 
            
            df.loc[df['RID'] == rid, 'user'] = user
            df.loc[df['RID'] == rid, 'esm_email'] = email[0]
            print_screen(rid)
            
        except:
            error = WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "sucessMessage"))
                )   
            print(error.text)
    
    df['result'] = df['EMAIL 1'] == df['esm_email']
    df['result'] = df['result'].apply(bool_check)
    print(df)
    return df
    
def bool_check(value):
    return 'user created' if value else 'error'           
            
if __name__ == "__main__":
    # Driver init
    driver = driver_init()
    username, password = user_credential()
    
    # Login
    login(username, password)
    
    # Load ESM Form
    df = load_esm_form()
    
    # create new column
    df['ems_check'] = ''
    df['ems_check'] = df['ems_check'].astype(str)
    
    # Check ESM before create
    rid_list = df['RID'].tolist()
    for rid in rid_list:
        write_response(df=df, hotel_rid=rid, response=check_esm_user(rid))
        
    print(df)
    
    # change this path
    excel_file_path = r'D:\NSANGKARN\OneDrive - ACCOR\Desktop\test.xlsx'
    
    # export and write again will remove this in the future
    df.to_excel(excel_file_path, index=False)
    df = pd.read_excel(excel_file_path, dtype=str)

    # compare data
    df['Temp_Column1'] = df['ems_check'].str.lower()
    df['EMAIL 1'] = df['EMAIL 1'].str.strip()
    df['Temp_Column2'] = df['EMAIL 1'].str.lower()

    # Compare the temporary columns and create a new column with Boolean values
    df['duplicate_check'] = df['Temp_Column1'] == df['Temp_Column2']

    # Drop the temporary columns
    df = df.drop(['Temp_Column1', 'Temp_Column2'], axis=1)

    # if esm check is "The search returned no results." create new = True, else false
    df['new_account'] = df['ems_check'].str.contains('The search returned no results.', case=False)

    
    # create delete first then create
    delete_then_create = df.query('new_account == False and duplicate_check == False')
    print(delete_then_create)
    # create new account
    create_new = df.query('new_account == True and duplicate_check == False')
    print(create_new)
    create_account(create_new)
    
    # delete account
    delete_esm(delete_then_create)
    create_account(delete_then_create)
    
    # get result with screen shot and write it to excel file
    
    result_df = get_screenshot(df=df)
    result_df.to_excel(excel_file_path, index=False)
    # Exit driver end of automation
    driver.quit()



