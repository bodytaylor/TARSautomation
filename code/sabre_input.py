from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os
import time
from hotel_content import ContentBook

hotel_content = ContentBook(r"C:\Users\NSANGKARN\bodytaylor\TARSautomation\hotel_workbook\B9F8\B9F8 Content Book Hotel Creation.xlsm")

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
    wait.until(EC.presence_of_all_elements_located((By.ID, element_id)))

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


## Need to work on this
def select_dropdown(element_id: str, value: str = None):
    if value:

        options = driver.find_elements(By.CSS_SELECTOR, "#null")

        for option in options:
            print(option.text)
            
def input_text(element_id: str, text: str = None):
    if text:
        text_area = driver.find_element(By.ID, element_id)
        text_area.send_keys(text)

def input_text_by_name(element_name: str, text: str = None):
    if text:
        text_area = driver.find_element(By.ID, element_name)
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
    postal_code = hotel_content.postal_code
    postal_code = hotel_content.remove_special_char(postal_code)
    
    # Phone
    phone = hotel_content.phone_country_code + hotel_content.phone
    phone = hotel_content.remove_special_char(phone)
    input_text_by_name('phone', phone)
    
    # Fax
    fax = hotel_content.phone_country_code + hotel_content.fax
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
    distance_mile = str((round((int(distance) * 0.621371), 0)))
    
    input_text('Airport_0', iata_code)
    select_dropdown('Direction_0', direction)
    input_text('Miles_0', distance_mile)
    
if __name__ == "__main__":
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    # Automation process
    username, password = user_credential()
    sebre_login(username, password)
    create_property(hotel_content)
    
    time.sleep(100)
    driver.quit()