from selenium import webdriver
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import time
import requests
import logging
import os
import sys
import urllib

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a StreamHandler to print log messages to the console
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)  # Set the level for console output

# Create a formatter for the console handler
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add the console handler to the root logger
logging.getLogger('').addHandler(console_handler)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

file_handler = logging.FileHandler(r'log\TarsAutomation.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# driver init
ieOptions = webdriver.IeOptions()
ieOptions.add_additional_option("ie.edgechromium", True)
ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
driver = webdriver.Ie(options=ieOptions)

def get_response_time(url: str) -> Union[float, None]:
    try:
        start_time = time.time()
        requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time
    except requests.RequestException as e:
        logger.error('Connection to DataWeb fail, Check User connection')
        return None, str(e)

# set delay according to server response
delay = get_response_time('https://dataweb.accor.net/')

def quit():
    driver.quit()
    logger.info('Closing the browser.')

# Load environment variables from .env file
def user_credential():
    load_dotenv()

    # Access the variables using os.environ.get()
    username = os.environ.get("TARSUSER")
    password = os.environ.get("PASSWORD")

    # Check if .env file exists
    if not (username and password):
        print("No credentials found. Please provide your credentials:")
        username = input("Username: ")
        password = input("Password: ")

        # Save the credentials to a new .env file
        with open(".env", "a") as env_file:
            env_file.write(f"TARSUSER={username}\n")
            env_file.write(f"PASSWORD={password}\n")

        print(".env file created with provided credentials.")
    else:
        logger.info(f"Credentials loaded from .env file. Username: {username}")
        
    return username, password  

def wait_for_element(element: str, by: By = By.ID, timeout: int = 10):
    try:
        WebDriverWait(driver, timeout * delay).until(
            EC.presence_of_element_located((by, element))
        )
        time.sleep(delay)
    except TimeoutError as e:
        logging.error(e)


def login():
    # Unpack Credential from function
    username, password = user_credential()
    
    driver.get("https://dataweb.accor.net/dotw-trans/login!input.action")
    try:
        # Wait for an element to be visible
        wait_for_element(element='login', by=By.NAME)

        # Find the username and password input fields and enter credentials
        username_field = driver.find_element(By.ID, "loginField")
        password_field = driver.find_element(By.NAME, "password")

        driver.execute_script("arguments[0].value = '';", username_field)
        username_field.send_keys(username)
        driver.execute_script("arguments[0].value = arguments[1];", password_field, password)
        
        # Press Login
        password_field.send_keys(Keys.RETURN)
        wait_for_element(element='searchButton', by=By.ID)
        logger.info(f'Login Success User: {username}')

    except TimeoutError:
        logger.info('User Session Timeout')
        # Retry login process
        login()
        
# set hotel rid

def hotel_search(hotel_rid: str):
    """
    Perform Hotel Search on Accor DataWeb

    This function automates the hotel search process on the Accor DataWeb platform using Selenium.
    It navigates to the hotel search page, enters the specified hotel ID (hotel_rid) into the search input,
    and retrieves the corresponding hotel name.

    Parameters:
    - hotel_rid: str
        The unique identifier of the hotel in Accor Network to be searched. Should be a string of exactly four letters.

    Returns:
    None

    Example:
    >>> hotel_search("A123")
    # Logs the selected hotel name or an error message if the hotel is not found within the allowed attempts.
    """
    
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    wait = WebDriverWait(driver, 10 * delay)

    try:
        # Locating and interacting with the search input field
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword"]')))
        search_input.clear()
        search_input.send_keys(f'{hotel_rid}')

        # Locating and interacting with the search button
        search_input.send_keys(Keys.RETURN)
        count = 0
        
        # Attempting to perform the search and retrieve the hotel name
        while True:
            action_res = response()

            if action_res is None:
                # Retrieving the hotel name if found
                hotel_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'hotelNameClass')))
                text = hotel_name.text
                logger.info(f'Selected Hotel : {text}')
                break
            elif count == 5:
                # Logging an error message if the hotel is not found after multiple attempts
                logger.error(f'Hotel not found : {hotel_rid}')
                break
            else:
                search_input.send_keys(Keys.RETURN)
                time.sleep(5 * delay)
            count += 1
                
    except TimeoutException as e:
        # Logging TimeoutError in case of element not found within the specified time
        logging.info(e)

        
def response():
    try:
        wait_for_element(element='//*[@id="actionmessage"]/ul/li/span', by=By.XPATH)
        span_element = driver.find_element(By.XPATH, '//*[@id="actionmessage"]/ul/li/span')
        span_text = span_element.text
        return span_text
    except:
        return None

def get_response(hotel_rid: str, code: str = ""):
    wait_for_element(element='//*[@id="messages"]', by=By.XPATH)
    action_message = get_message()
    error_message = get_error_message()
    message = action_message or error_message
    logger.info(f'{hotel_rid} : {code} : {message}')

def get_message() -> str:
    try:
        action_message_element = driver.find_element(By.XPATH, '//*[@id="actionmessage"]')
        message = action_message_element.find_element(By.TAG_NAME, 'span').text
        return message
    except:
        return None
    
def get_error_message() -> str:
    try:
        error_message_element = driver.find_element(By.XPATH, '//*[@id="errormessage"]')
        message = error_message_element.text
        return message
    except:
        return None

# go to specific url and wait for page title to load
def get(url: str):
    driver.get(url)
    element = WebDriverWait(driver, 10 * delay).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'h2'))
    )
    logger.info(element.text)

def add_language(lang: list):
    script = f"window.confirm = ajaxReplace('dataForm', 'addHotelLanguage.action?language.languageCode={lang}', 'get');"
    driver.execute_script(script)
    logger.info(f'{lang} Added')
    time.sleep(delay)

# input textbox
def input_text(element_id: str, text: str):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        logger.info(f'{element_id} : {text}')
    
# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        logger.info(f'{element_id} : {value}')
        
# click button
def click_button(element):
    driver.execute_script(f'document.getElementById("{element}").click();')
    logger.info('Submitdata')
    time.sleep(1.5 * delay)

# Tickbox in browser console
def tick_box(element, value='Checked'):
    if value is not None:
        driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
        logger.info(f'{element} : checkbox.checked')
  
# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        script = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return script
    else:
        return None
    
def translate_hotel_product(option: int = 1, element_id='translateHotelProductForm'):
    if option == 1:
        # Click on Translate button
        script = f"""
        document.getElementById('{element_id}.submitButton').click();
        """
    
        driver.execute_script(script)
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    else:
        script = f"""
        document.getElementById('{element_id}.submitSaveButton').click();
        """
        driver.execute_script(script)
        time.sleep(1)

# for product translation
def clear_marketing_box():
    driver.execute_script("document.getElementById('hotelProductTranslate.referenceLabel').value = '';")

def clear_description_box():
    driver.execute_script("document.getElementById('hotelProductTranslate.description').value = '';")

# Enter Translations
def product_description(code: str, type: str, description: str, marketing: str, hotel_rid: str):
    """
    Update product description and marketing label on the translation page.

    Args:
    - code (str): The product code.
    - type (str): The product type code.
    - description (str, optional): The product description to be updated. If None, the description is not updated.
    - marketing (str, optional): The marketing label to be updated. If None, the marketing label is not updated.
    - hotel_rid (str): The hotel RID.

    Returns:
    - None: This function does not return any value.

    Raises:
    - No specific exceptions are raised.

    Note:
    - This function opens a web browser on the translation page and waits for the webpage to load.
    - It then operate the description input box, types in the provided description and marketing label (if provided),

    Example usage:
    ```python
    # Update product description and marketing label
    product_description('TWA', 'ROOMTW', 'New Description', 'New Procut Marketing Lavel', 'A123')

    # Update only product description
    product_description('TWA', 'ROOMTW', 'Updated Description', None, 'A123')

    # Update only marketing label
    product_description('TWA', 'ROOMTW', None, 'Product Marketing Label', 'A123')
    ```
    """
    
    # Open Web Browser on translate page and wait for webpage load
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={code}&hotelProduct.type.code={type}&hotelProduct.centralUse=true&'
    get(url)
    
    # Open description input box
    driver.execute_script(f"displayTranslateForm('translateInput','GB','{code}','{type}','{hotel_rid}','productsDescriptionsTable','true','true','GB','true')")
    # Wait for page to load
    wait_for_element('translateHotelProductForm')
    
    # find description box
    description_box = driver.find_element(By.ID, "hotelProductTranslate.description")
    marketing_box =  driver.find_element(By.ID, "hotelProductTranslate.referenceLabel")
         
    # Get data from DataFrame and type in the discription box, do not change the secound locater!
    if description != None:
        clear_description_box()
        description_box.send_keys(description)
        time.sleep(0.5)

    # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
    if marketing != None:   
        clear_marketing_box()
        marketing_box.send_keys(marketing)
        time.sleep(0.5)
        
    
# find type of product
def find_type(df, code):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        return result[2]
    else:
        return None
    
# Purse text in to url
def url_parse(input):
    url_encoded = urllib.parse.quote_plus(input)
    return url_encoded