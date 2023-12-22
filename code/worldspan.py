from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import pandas as pd
import time
import csv
import os

def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

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
    

def get_dropdown(element_id=str):
    try:
        select = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f'{element_id}'))
        )
        select = driver.find_element(By.ID, f'{element_id}')
        selected_option_text = select.find_element(By.CSS_SELECTOR, 'option[selected="selected"]').text
        print(f"{element_id}: {selected_option_text}")
        return selected_option_text
    except ValueError as e:
        print(e)


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

# login
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
        span_element = driver.find_element(By.CLASS_NAME, "hotelNameClass")
        text = span_element.text.strip()
        print(text)
        return None

def hotel_search(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
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
        print('Hotel Found!')    
        
def check_available(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]'))
        )
        element = driver.find_element(By.XPATH, '//*[@id="keyword"]')
        element.clear()
        element.send_keys(f'{hotel_rid}')
        search_button = driver.find_element(By.ID, 'searchButton')
        
        while True:
            search_button.click()
            action_res = response()
            time.sleep(2)

            if (action_res == 'No hotels found with the keywords used'):
                print(f'[INFO] - World span code is valid: {hotel_rid[3:]}')
                break
            else:
                print(f'[INFO] - {hotel_rid} Code not available Please use another one')
                break
    except ValueError as e:
        print(e)   
        
# Go to General page
def get_general_page():
    driver.get('https://dataweb.accor.net/dotw-trans/displayGeneralInformation!input.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'formTitle'))
        )
        count = 0
        
        while True:
            element = driver.find_element(By.ID, 'formTitle')
            text = element.text
            time.sleep(2)
            count += 1
            
            if (text == 'General Information') or (count == 5):
                break
            else:
                driver.refresh()
    except ValueError as e:
        print(e)   
        
# Standard Dic
standard_dict = {
    "21c MUSEUM HOTELS": "LH",
    "25HOURS": "UP",
    "ADAGIO ACCESS": "MD",
    "ADAGIO ORIGINAL": "EY",
    "ADAGIO PREMIUM": "UP",
    "ALL SEASONS": "EY",
    "ANGSANA": "UP",
    "ART SERIES": "UP",
    "BANYAN TREE": "LH",
    "BREAKFREE": "EY",
    "BY MERCURE": "MD",
    "CASSIA": "MD",
    "DELANO": "MD",
    "DHAWA": "LH",
    "ETAP HOTEL": "BU",
    "FAENA": "LH",
    "FAIRMONT": "LH",
    "FOLIO": "MD",
    "GARRYA": "MD",
    "GRAND MERCURE": "UP",
    "GREET": "EY",
    "HANDWRITTEN": "MD",
    "HOMM": "MD",
    "HOTELF1": "BU",
    "HYDE": "LH",
    "IBIS BU": "BU",
    "IBIS HOTELS": "EY",
    "IBIS STYLES": "EY",
    "JO&JOE": "BU",
    "MAMA SHELTER": "MD",
    "MANTRA": "MD",
    "MANTIS": "UP",
    "MERCURE": "MD",
    "MERCURE LIVING": "MD",
    "MGALLERY BY SOFITEL": "LH",
    "MONDRIAN": "LH",
    "MORGANS ORIGINALS": "LH",
    "Mövenpick": "UP",
    "MOVENPICK LIVING": "UP",
    "NOVOTEL": "MD",
    "NOVOTEL LIVING": "MD",
    "NOVOTEL SUITES": "MD",
    "PEPPERS": "UP",
    "PULLMAN": "UP",
    "RAFFLES": "LH",
    "RIXOS HOTELS": "LH",
    "SLS": "LH",
    "SO SOFITEL": "LH",
    "SOFITEL": "LH",
    "SOFITEL LEGEND": "LH",
    "SWISSOTEL": "UP",
    "SWISSOTEL LIVING": "UP",
    "THE SEBEL": "UP",
    "TRIBE": "MD",
}

chain_code = {
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

# download excel data file
def get_rate_level():
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelRates.action')
    time.sleep(2)
    try:
        download_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//a[img[@title="Excel"]]'))
        )
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, '//a[img[@title="Excel"]]')
        download_button.click()
        time.sleep(1.5)
        file_path = 'temp\\table-data.xls'
        df = pd.read_excel(file_path)
        # remove file
        import os
        os.remove(file_path)
        return df
    except TimeoutException as e:
        get_rate_level()

def meal_plan(df):
    meal_option = []
    ra = df[df['Rate level code'].str.contains('RA')]
    rb = df[df['Rate level code'].str.contains('RB')]
    rh = df[df['Rate level code'].str.contains('RH')]
    rf = df[df['Rate level code'].str.contains('RF')]
    ri = df[df['Rate level code'].str.contains('RI')]
    if len(ra) != 0:
        meal_option.append('EP')
    if len(rb) != 0:
        meal_option.append('BB')
    if len(rh) != 0:
        meal_option.append('HB')
    if len(rf) != 0:
        meal_option.append('FB')
    if len(ri) != 0:
        meal_option.append('FB')
    return meal_option

def get_surrounding():
    driver.get('https://dataweb.accor.net/dotw-trans/ipTabs!input.action')
    time.sleep(2)
    try:
        download_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//a[img[@title="Excel"]]'))
        )    
        time.sleep(1)    
        download_button = driver.find_element(By.XPATH, '//a[img[@title="Excel"]]')
        download_button.click()
        time.sleep(1.5)
        file_path = 'temp\\table-data.xls'
        df = pd.read_excel(file_path)
        # remove file
        import os
        os.remove(file_path)
        return df
    except TimeoutException as e:
        get_surrounding()
        
def get_checkin_time():
    driver.get('https://dataweb.accor.net/dotw-trans/secure/displayHotelSalesConditions!input.action?&salesConditionTypeSelected=CINPOL')
    time.sleep(2)
    try:
        download_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelSalesConditionsTable"]/thead/tr[1]/td/table/tbody/tr/td[8]/a'))
        )
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, '//*[@id="hotelSalesConditionsTable"]/thead/tr[1]/td/table/tbody/tr/td[8]/a')
        download_button.click()
        time.sleep(1.5)
        import os
        directory_path = 'temp'
        file_list = [file for file in os.listdir(directory_path) if file.endswith('.xls')]
        file_to_open = os.path.join(directory_path, file_list[0])
        df = pd.read_excel(file_to_open)
        # remove file
        os.remove(file_to_open)
        
        filtered_df = df[df['Level'] == 'H']
        checkin_time = filtered_df['Start'].values[0]
        checkin_time = str(checkin_time).replace(':', '')
        return checkin_time
    except TimeoutException as e: 
        get_checkin_time() 
    
def get_checkout_time():
    driver.get('https://dataweb.accor.net/dotw-trans/secure/displayHotelSalesConditions!input.action?&salesConditionTypeSelected=COUPOL')
    time.sleep(2)
    try:
        download_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelSalesConditionsTable"]/thead/tr[1]/td/table/tbody/tr/td[8]/a'))
        )
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, '//*[@id="hotelSalesConditionsTable"]/thead/tr[1]/td/table/tbody/tr/td[8]/a')
        download_button.click()
        time.sleep(1.5)
        import os
        directory_path = 'temp'
        file_list = [file for file in os.listdir(directory_path) if file.endswith('.xls')]
        file_to_open = os.path.join(directory_path, file_list[0])
        df = pd.read_excel(file_to_open)
        # remove file
        os.remove(file_to_open)
        
        filtered_df = df[df['Level'] == 'H']
        checkout_time = filtered_df['Start'].values[0]
        checkout_time = str(checkout_time).replace(':', '')
        return checkout_time
    except TimeoutException as e:
        get_checkout_time()


if __name__ == "__main__":     
    
    # create code
    hotel_rid = input('Please Input Hotel RID: ')
    hotel_rid = hotel_rid.upper()
    amadeus = input(f'Please Input Amadeus Code for {hotel_rid}: ')

    # Setup Chrome Driver
    chrome_options = webdriver.ChromeOptions()
    ### Will test and upgrade this line soon ###
    prefs = {"download.default_directory": r"C:\Users\NSANGKARN\bodytaylor\TARSautomation\temp"}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # Login
    username, password = user_credential()
    login(username, password)
    hotel_search(hotel_rid=hotel_rid)
    checkin = get_checkin_time()
    checkout = get_checkout_time()
    # get data
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')
    time.sleep(1)
    # chain
    hotel_chain = get_data(element_id='hotel.chain.code')
    # Chain Code
    amadeus_chain_code = chain_code.get(hotel_chain)
    if amadeus_chain_code is None:
        amadeus_chain_code = 'RT'
        
    worldspan_code = amadeus_chain_code + amadeus[3:5] + amadeus[0:3]
    tars_check_code = 'tw*' + amadeus[3:5] + amadeus[0:3]
    # name
    hotel_name = get_data('hotel.name')
    # primary airport
    # address 1st line street name and number only
    address_1 = get_data('hotel.address.addresses[0]')
    address_1 = str(address_1).replace('-', ' ')
    address_2 = get_data('hotel.address.addresses[1]')
    address_2 = str(address_2).replace('-', ' ')
    address_3 = get_data('hotel.address.addresses[2]')
    address_3 = str(address_3).replace('-', ' ')

    # tran (Y) if hotel check shuttle available for AER1
    # FAM PLAN (Y) if CHIPOL at H level is set
    # adress 2nd line city + country + zipcode
    city = get_data('hotel.address.city')
    country_code = get_data('hotel.address.country.code')
    zip_code = get_data('hotel.address.zipCode')
    zip_code = str(zip_code).replace('-', '')
    country = get_dropdown('hotel.address.country.code')

    # Checkin time format 0000
    # ST skip
    # CTRY C + 2 letters country code
    ctry = 'C' + country_code
    # POSTAL CODE is the zip code?
    # Checkout time format 0000
    # Phone 
    phone_index = get_data('hotel.address.indTel')
    phone = get_data('hotel.address.tel')
    f_phone = str(phone_index) + str(phone)
    # COMM PERCENT 10
    commission = '10'
    # FAX 
    fax = get_data('hotel.address.fax')
    f_fax = str(phone_index) + str(fax)
    # MEAL PLAN
    # TAX RATE 00 except JAPAN 0
    if country_code == 'JP':
        tax_rate = '0'
    else:
        tax_rate = '15'
    # PROPERTY TYPE CODE EY, LH, MD, UP
    brand_code = get_dropdown('hotel.brand.code')
    property_type = standard_dict.get(brand_code)

    surrounding = get_surrounding()
    result = surrounding[surrounding['Code'] == 'AER1']
    primary_airport = result['Name'].values[0]
    shuttle_service = result['Shuttle'].values[0]
    if shuttle_service == False:
        shuttle = 'N'
    else:
        shuttle = 'Y'

    address_line2 = f'{city} {country} {zip_code}'

    check_meal = get_rate_level()
    meal_option = meal_plan(check_meal)

    get_general_page()
    currency = get_data('selectCurrency')
    total_room = get_data('gi.nbOfRooms')

    check_available(hotel_rid=tars_check_code)
        
    driver.quit()

    # Check file directory
    directory_path = r"gds\worldspan"
    create_directory(directory_path)

    # write to csv
    file_path = f"gds\worldspan\{hotel_rid} Worldspan.csv"
    header = ['NAME', 'PRIM AIRPORT', 'ADDRESS', 'TRANS', 'FAM PLAN', 'ADDRESS_2', 'CHECK-IN',
            'ST', 'CNTRY', 'POSTAL CODE', 'CHECK OUT', 'PHONE', 'TELEX', 'COMM PERCENT',
            'FAX', 'RESV', 'MEAL PLAN', 'TAX RATE', 'PROPERTY TYPE CODES', 'CURR', 'TOTAL RMS',
            'RA', 'RC', 'CR', 'EX', 'EC', 'worldspan code', 'Check availability']

    with open(file_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow([hotel_name, primary_airport, address_1, shuttle, 'Y', address_line2, str(checkin),
                            '', ctry, str(zip_code), str(checkout), str(f_phone), '', '10', 
                            str(f_fax), '', meal_option, str(tax_rate), property_type, currency, total_room,
                            'K', 'K', 'K', 'K', 'K', worldspan_code, f'HHPC{worldspan_code}'])

