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
from hotel_content import ContentBook

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
        
def create_property(hotel_content):
    wait_element(element_id='footer0')
    driver.execute_script("submitNavigForm('propertyCreate', 'PropertyList', 'create', '', 'true', '');")
    data_entry(hotel_content)
    
def data_entry(hotel_content):
    # Owning Property Group (Dropdown)
    sabre_chain = hotel_content.get_partner_chain_code()
    select_dropdown('propertyGroup', value=sabre_chain)
    
    # Cross Reference
    input_text_by_name('crossRef', hotel_content.hotel_rid)
    
    # Property Name
    input_text_by_name('propertyName', hotel_content.hotel_name)
    
    # Long Property Name
    input_text_by_name('longPropertyName', hotel_content.hotel_commercial_name)
    
    # Address1
    input_text_by_name('address1', hotel_content.address1)
    # Address2
    input_text_by_name('address2', hotel_content.address2)
    # Address3
    input_text_by_name('address3', hotel_content.address3)
    
    # City
    input_text_by_name('city', hotel_content.city)
    
    # Country (Dropdown)
    country_code = hotel_content.get_country_code()
    select_dropdown('countryCode', value=country_code)
    
    # State/Province (Dropdown) -> skip for now
    
    # Postal Code
    postal_code = str(hotel_content.zip_code)
    postal_code = hotel_content.remove_special_char(postal_code)
    input_text_by_name('postalCode', postal_code)
    
    # Phone
    phone = str(hotel_content.phone_country_code) + str(hotel_content.phone)
    phone = hotel_content.remove_special_char(phone)
    input_text_by_name('phone', phone)
    
    # Fax
    fax = str(hotel_content.phone_country_code) + str(hotel_content.fax)
    if len(fax) >= 3:
        input_text_by_name('fax', fax)
    
    # currency (Dropdown)
    select_dropdown('currency', value=hotel_content.currency_code)
    
    # URL
    input_text_by_name('url', hotel_content.hotel_url)
    
    # Airport km -> mile
    iata_code = hotel_content.main_attractions['AER1'][0]
    direction = hotel_content.main_attractions['AER1'][1]
    distance = hotel_content.main_attractions['AER1'][4]
    distance_mile = str((int((int(distance) * 0.621371))))
    
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
    driver.execute_script("submitNavigForm('propertySearch', 'PropertySearch', '', '', 'true', '');")
    wait_element(element_id='searchCriteria')
    input_text_by_name('propertyNbr', sabre_id)
    
    # Search and wait for element
    driver.execute_script("searchPressed();")
    wait_element(element_id='displayTableModelTable')
    
    # tickbox 
    driver.execute_script("document.querySelector('input[name=SELECT]').checked = true;")
    
    # Modify property
    driver.execute_script('modifyPressed();')
    
    # Change dropdown to property
    wait_element(element_id='disableCode')
    dropdown = driver.find_element(By.NAME, 'disableCode')
    select = Select(dropdown)
    select.select_by_index(0)
    
    # Submit
    driver.execute_script('commitPressed();')
    
if __name__ == "__main__":
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    # Migrate the code to Accor repo for better workflow, sometime we get a request from Audit team
    rid = str(input('Input Hotel RID: '))
    hotel_content = ContentBook(f"hotel_workbook\{rid}\{rid} Content Book Hotel Creation.xlsm")
    
    # Automation process
    username, password = user_credential()
    sebre_login(username, password)
    # sabre_id = create_property(hotel_content)
    sabre_id = data_entry(hotel_content)
    active_property(sabre_id)
    
    # Job Summary part
    # Create Logfile here
    driver.quit()