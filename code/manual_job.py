from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import functions as fn
import csv
import time

def get_data(element_id=str):
    try:
        element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f'{element_id}'))
        )
        data = element.get_attribute("value")
        print(data)
    except:
        print("Page did not load correctly. Element not found.")
    return data


chrome_options = Options()
# chrome_options.add_argument("--headless")  # Enable headless mode
driver = webdriver.Chrome(options=chrome_options)

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
        submit_button.click()
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
        print("Response Message Not Found!.")
        return None
    finally:
        print(span_text)
        
        
def hotel_search(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]'))
        )
        element = driver.find_element(By.XPATH, '//*[@id="keyword"]')
        element.clear()
        element.send_keys(f'{hotel_rid}')
        search_button = driver.find_element(By.ID, 'searchButton')
        count = 0
        
        while True:
            search_button.click()
            action_res = response()
            time.sleep(2)
            count += 1
            
            if (action_res != 'No hotels found with the keywords used') or (count == 5):
                break
    except:
        print("Page did not load correctly. Element not found.")    
        
def add_cinpol():
    driver.get('https://dataweb.accor.net/dotw-trans/secure/displayHotelSalesConditions!input.action?&salesConditionTypeSelected=CINPOL&')   
    
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//a[img[@title="Add"]]'))
        )
        element = driver.find_element(By.XPATH, '//a[img[@title="Add"]]')
        element.click()  
        time.sleep(1)
        element_h =  driver.find_element(By.ID, 'h')
        element_h.click()
        element_no_lim = driver.find_element(By.XPATH, '//*[@id="validityPeriod"]/table/tbody/tr/td[3]/button')
        element_no_lim.click()
        element_all_day = driver.find_element(By.XPATH, '//*[@id="button1"]')
        element_all_day.click()
        text_box = driver.find_element(By.XPATH, '//*[@id="cdv.hour"]')
        text_box.send_keys('15:00')
        add_but = driver.find_element(By.ID, 'addSalesConditionButton')
        add_but.click()
        time.sleep(2)
        translation = driver.find_element(By.XPATH, '//*[@id="hotelSalesConditionsTable_row3"]/td[2]/a')
        translation.click()
        dropdown = Select(driver.find_element(By.ID, 'scriptTypeSelect'))
        dropdown.select_by_value('CINP01')
        click_add = driver.find_element(By.ID, 'mergeButton')
        click_add.click()
        time.sleep(3)
    except Exception as e:
        print(e)
        
hotel_rid = input('input RID: ' )
hotel_rid_list = str(hotel_rid).split()

username, password = user_credential()
login(username, password)
for hotel in hotel_rid_list:
    hotel_search(hotel_rid=hotel)
    add_cinpol()
    
driver.quit()