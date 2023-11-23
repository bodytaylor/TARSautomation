from functions import *
import pyautogui as pa
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import functions as fn
import time

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


def login():
        # Navigate to the login page
    driver.get("https://dataweb.accor.net/dotw-trans/login!input.action")

    # Wait for an element to be visible
    try:
        username_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "login"))
        )
            # Find the username and password input fields and enter your credentials
        username_field = driver.find_element(By.ID, "loginField")
        password_field = driver.find_element(By.NAME, "password")

        username = "NANSAN"
        password = "Welcome@2023"
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
        print('Hotel Found!')    
        
def check_available(hotel_rid):
    driver.get('https://dataweb.accor.net/dotw-trans/selectHotelInput.action')
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 5).until(
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
        element = WebDriverWait(driver, 5).until(
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

# download excel data file
def get_rate_level():
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelRates.action')
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
    except ValueError as e:
        print(e)

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
    except ValueError as e:
        print(e)
        
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
    except ValueError as e:
        print(e)    
    
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
    except ValueError as e:
        print(e)  

# Take Now Hotel    
hotel_list = ['C1N7']

# write to csv
for hotel in hotel_list:
    # Setup Chrome Driver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    login()
    hotel_search(hotel_rid=hotel)
    # get data
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')
    time.sleep(1)
    # chain
    hotel_chain = get_data(element_id='hotel.chain.code')
    # name
    hotel_name = get_data('hotel.name')
    city_code = get_data('hotel.iataCityCode')
    city_name = get_data('hotel.address.city')
    country_code = get_data('hotel.address.country.code')
        
    driver.quit()

    # for input day 1 Galileo
    # Make sure you are in the right chain
    time.sleep(2)
    find_and_click(img_path=r"img\gds_goto.PNG")
    tabing(7)
    pa.typewrite(hotel_name)
    tabing(1)
    pa.typewrite(city_code)
    tabing(1)
    pa.typewrite(city_name)
    time.sleep(1)
    tabing(2)
    pa.typewrite(country_code)
    
    time.sleep(1)
    pa.press('enter')
    time.sleep(3)
    pa.screenshot(f"gds\galileo\{hotel}_galileo.png")
