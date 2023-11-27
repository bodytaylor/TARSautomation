from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
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

# Chain Code
chain_code = {
    'BY': 'BAN',
    'EN': '21C',
    'EN': 'TWF',
    'EN': 'DEL',
    'EN': 'HYD',
    'EN': 'MSH',
    'EN': 'MOD',
    'EN': 'TOR',
    'EN': 'SLS',
    'EN': 'SO',
    'FA': 'FAR',
    'SB': 'SOF',
    'SB': 'MGR',
    'PU': 'PUL',
    'PU': 'PLL',
    'YR': 'RAF',
    'RX': 'RIX',
    'SL': 'SWI',
}

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
        
         
def create_amadeus_code(hotel_rid):

    # Navigate to the page
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')

    # Property code get from data web
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'hotel.longCode'))
        )
        hotel_longcode = element.get_attribute("value")
        hotel_longcode = str(hotel_longcode).replace("/", "")
        print(hotel_longcode)
    except:
        print("Page did not load correctly. Element not found.")
        
    # Property name
    hotel_name = get_data(element_id='hotel.name')
        
    # Currency 3 letter
    path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    # Surrounding Attraction /Use Orientation information of code CENT
    location_data = fn.get_excel_values(file_path=path,
                                        sheet_name='Main Attractions',
                                        cell_addresses=['G18']
                                        )

    cent = location_data[0] 
    if cent is not None:
        cent_cap = ""
        for char in cent:
            if char.isupper():
                cent_cap += char
    else:
        cent_cap = 'N'

    # Surrounding Attraction  - Use Orientation information of code AER1 Defult T
    aer1 = 'T'

    # Address 2 Lines can combine from 3 lines
    address_1 = get_data(element_id='hotel.address.addresses[0]')
    address_2 = get_data(element_id='hotel.address.addresses[1]')
    address_3 = get_data(element_id='hotel.address.addresses[2]')
    address_2 = f'{address_2}, {address_3}'

    # City Name
    city = get_data(element_id='hotel.address.city')

    # Zip Code
    zip_code = get_data(element_id='hotel.address.zipCode')

    # State code - Only AR, AU, BR, CA, US, IN (2-A)
    # Country Code 2 digit
    country_code = get_data(element_id='hotel.address.country.code')

    # Phone Number format (index) number
    p_index = get_data(element_id='hotel.address.indTel')
    p = get_data(element_id='hotel.address.tel')
    phone = f'({p_index}) {p}'

    # Fax Number format (index) number
    f_index = get_data(element_id='hotel.address.indFax')
    f = get_data(element_id='hotel.address.fax')
    fax = f'({f_index}) {f}'

    # get chain code
    hotel_chain = get_data(element_id='hotel.chain.code')
    amadeus_chain_code = chain_code.get(hotel_chain)

    if amadeus_chain_code is None:
        amadeus_chain_code = 'RT'
    print(amadeus_chain_code)

    # Check code available with DATA WEB 1A*IATA + IDENTIFIER
    driver.get('https://dataweb.accor.net/dotw-trans/secure/selectHotel!input.action')
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]'))
        )
        hotel_search = driver.find_element(By.XPATH, '//*[@id="keyword"]')
        hotel_search.clear()
        hotel_search.send_keys(f'1A*{hotel_longcode}')
        search_button = driver.find_element(By.ID, 'searchButton')
        search_button.click()
    except:
        print("Page did not load correctly. Element not found.")

    code_not_available = {}
    
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]/ul/li/span'))
        )
        span_element = element.find_element(By.XPATH, '//*[@id="actionmessage"]/ul/li/span')
        span_text = span_element.text
        print(span_text)
    except:
        print("Page did not load correctly. Element not found.")
    finally:
        if span_text != 'No hotels found with the keywords used':
            code_not_available[hotel_rid] = hotel_longcode

    # Currency
    driver.get('https://dataweb.accor.net/dotw-trans/displayGeneralInformation!input.action')
    currency = get_data(element_id='selectCurrency')

    # Check code available with GDS emulater format HF + CHAIN CODE + IATA + IDENTIFIER 
    amadeus_check_code = f'HF{amadeus_chain_code}{hotel_longcode}'
    amadeus_code = f'{amadeus_chain_code}{hotel_longcode}'
    print(amadeus_check_code)

    # write data to csv file
    file_path = f"gds\{hotel_rid} Amadeus.csv"
    header = ['Property Code', 'Property Name', 'Currency code', 'Location code', 
            'Transportation code', 'AddressLine1', 'AddressLine2', 'CityName','State code', 'Zipcode', 
            'Region code', 'Country code', 'Phone number', 'Fax number', 'Amadeus Check Code']

    with open(file_path, mode="w", newline="") as csv_file:

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow([amadeus_code, hotel_name, currency, cent_cap, 
                            aer1, address_1, address_2, city, '', zip_code,
                            '', country_code, phone, fax, amadeus_check_code])

hotel_rid = input('input RID: ' )
hotel_rid_list = str(hotel_rid).split()

username, password = user_credential() 
login(username, password)
for hotel in hotel_rid_list:
    hotel_search(hotel_rid=hotel)
    
driver.quit()