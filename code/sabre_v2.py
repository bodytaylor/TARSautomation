from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from dotenv import load_dotenv
import os
import time
import re
from accor_repo import AccorRepo

# Load environment variables from .env file
def user_credential():
    load_dotenv()

    # Access the variables using os.environ.get()
    username = os.environ.get("SABREUSER")
    password = os.environ.get("SABREPASSWORD")

    # Check if .env file exists
    if not (username and password):
        print("No .env file found. Please provide your credentials:")
        username = input("Sabre Username: ")
        password = input("Sabre Password: ")

        # Save the credentials to a new .env file
        with open(".env", "a") as env_file:
            env_file.write(f"SABREUSER={username}\n")
            env_file.write(f"SABREPASSWORD={password}\n")

        print(".env file created with provided credentials.")
    else:
        print(f"Credentials loaded from .env file. Username: {username}")
        
    return username, password

def wait_element(element_id: str, limit: int = 30):
    wait = WebDriverWait(driver, limit)
    wait.until(EC.visibility_of_element_located((By.ID, element_id)))

def sebre_login(username, password):
    driver.get('https://hotels.cert.sabre.com/login.jsp')
    wait_element(element_id='userID')
    
    # find user pass aff box
    user_box = driver.find_element(By.ID, "userID")
    password_box = driver.find_element(By.ID, "password")
    affiliate = driver.find_element(By.ID, "affiliate")
    submit_button = driver.find_element(By.NAME, 'Submit')
    
    # input credential
    user_box.send_keys(username)
    password_box.send_keys(password)
    affiliate.send_keys('ACCOR')
    submit_button.click()

# Extract sabre id from alert text
def extract_number(text: str):
    numbers = re.findall(r'\d+', text)

    if numbers:
        extracted_number = int(numbers[0])
        return extracted_number
    else:
        print("No numbers found in the text.")


## Need to work on this
def select_dropdown(element_id: str, value: str = None):
    if value:
        dropdown = driver.find_element(By.NAME, element_id)
        select = Select(dropdown)
        select.select_by_value(value)

def input_text(element_id: str, text: str = None):
    if text:
        text_area = driver.find_element(By.ID, element_id)
        text_area.send_keys(text)

def input_text_by_name(element_name: str, text: str = None):
    if text:
        text_area = driver.find_element(By.NAME, element_name)
        text_area.send_keys(text)
        
def create_property(rid):
    wait_element(element_id='footer0')
    driver.execute_script("submitNavigForm('propertyCreate', 'PropertyList', 'create', '', 'true', '');")
    wait_element('level0')
    data_entry(rid)
    
def get_partner_chain_code(hotel_chain):
    partner_code = {
        'BAN': 'BY', 
        '21C': 'EN', 
        'TWF': 'EN', 
        'DEL': 'EN', 
        'HYD': 'EN', 
        'MSH': 'EN', 
        'MOD': 'EN', 
        'TOR': 'EN', 
        'SLS': 'EN', 
        'SO': 'EN', 
        'FAR': 'FA', 
        'SOF': 'SB', 
        'MGR': 'SB', 
        'PUL': 'PU', 
        'PLL': 'PU', 
        'RAF': 'YR', 
        'RIX': 'RX', 
        'SWI': 'SL'
        }

    code = partner_code.get(hotel_chain)
    
    if code is None:
        code = 'RT'
    return code

def remove_special_char(input_string):
# Use regex to remove all non-alphanumeric characters
    result_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    return result_string
    
# Update data source from content book to accor repo
def data_entry(rid):
    hotel_content = AccorRepo(rid)
    # Owning Property Group (Dropdown)
    hotel_content.get_hotel_info()
    hotel_content.get_hotel_address()
    
    hotel_chain = hotel_content.brand_code
    sabre_chain = get_partner_chain_code(hotel_chain)
    select_dropdown('propertyGroup', value=sabre_chain)
    
    # Cross Reference
    input_text_by_name('crossRef', rid)
    
    # Property Name
    input_text_by_name('propertyName', hotel_content.hotel_name)
    
    # Long Property Name
    input_text_by_name('longPropertyName', hotel_content.hotel_commercial_name)
    
    # Address1
    input_text_by_name('address1', hotel_content.address1)
    # Address2
    if hotel_content.address2 is not None:
        input_text_by_name('address2', hotel_content.address2)
    # Address3
    if hotel_content.address3 is not None:
        input_text_by_name('address3', hotel_content.address3)
    
    # City
    input_text_by_name('city', hotel_content.city)
    
    # Country (Dropdown)
    country_code = hotel_content.country_code
    select_dropdown('countryCode', value=country_code)
    
    # State/Province (Dropdown) -> skip for now
    
    # Postal Code
    postal_code = str(hotel_content.post_code)
    postal_code = remove_special_char(postal_code)
    input_text_by_name('postalCode', postal_code)
    
    # Phone
    phone = str(hotel_content.phone_code) + str(hotel_content.phone)
    phone = remove_special_char(phone)
    input_text_by_name('phone', phone)
    
    # Fax
    if hotel_content.fax is not None:
        fax = str(hotel_content.phone_code) + str(hotel_content.fax)
        input_text_by_name('fax', fax)
    
    # currency (Dropdown)
    select_dropdown('currency', value=hotel_content.currency)
    
    # URL
    hotel_web_address = f'http://all.accor.com/{rid}'
    input_text_by_name('url', hotel_web_address)
    
    # Airport km -> mile
    hotel_content.get_iata()
    iata_code = hotel_content.airport_name
    direction = hotel_content.airport_direction
    distance_mile = str(hotel_content.airport_distance_m)
    
    input_text('Airport_0', iata_code)
    select_dropdown('Direction_0', direction)
    input_text('Miles_0', distance_mile)
    
    # submit
    driver.execute_script('commitPressed();')
    time.sleep(3)
    
    # Read browser aleart
    alert = Alert(driver)
    message = alert.text
    print(message)
    alert.accept()
    sabre_id = extract_number(message)
    return sabre_id
    
def active_property(sabre_id: str):
    time.sleep(3)
    driver.execute_script("submitNavigForm('propertySearch', 'PropertySearch', '', '', 'true', '');")
    wait_element(element_id='searchCriteria')
    input_text_by_name('propertyNbr', sabre_id)
    
    # Search and wait for element
    driver.execute_script("searchPressed();")
    time.sleep(2)
    
    # tickbox 
    driver.execute_script("document.querySelector('input[name=SELECT]').checked = true;")
    
    # Modify property
    driver.execute_script('modifyPressed();')
    
    # Change dropdown to property
    wait_element(element_id='level1')
    time.sleep(1)
    dropdown = driver.find_element(By.NAME, 'disableCode')
    select = Select(dropdown)
    select.select_by_index(0)
    
    # Submit
    driver.execute_script('commitPressed();')
    time.sleep(1)
    print(f'{sabre_id} Property has been activated on Sabre.')
    
if __name__ == "__main__":
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    # Migrate the code to Accor repo for better workflow, sometime we get a request from Audit team
    rid = str(input('Input Hotel RID: '))
    
    # Automation process
    username, password = user_credential()
    sebre_login(username, password)
    sabre_id = create_property(rid)
    active_property(sabre_id)
    
    # Job Summary part
    # Create Log file here
    driver.quit()