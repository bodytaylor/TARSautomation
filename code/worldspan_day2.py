from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import pandas as pd
import time
import pyautogui
import functions as f
import datetime
import os

# Further update will be text processing. worldspan has limit per line input!!

# find opposite direction
def find_opposite_dir(direction):
    opposite_direction = {
    'N': 'S',
    'S': 'N',
    'W': 'E',
    'E': 'W'
    }
    
    opp_orientation = ''
    try:
        for i in direction:
            opp_orientation += opposite_direction.get(i)
        return opp_orientation
    except:
        return 'N'

# for save Worldspand data
def save():
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.press('up')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('HUE')
    pyautogui.press('enter')
    time.sleep(1)
    
def type_with_delay(text, delay=0.5):
    text = str(text)
    pyautogui.typewrite(text)
    time.sleep(delay)
    
def find_gds_windows():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\worldspan_main.PNG", confidence=0.85)
    print('Please Open GDS - Term Worldspan Prod')
    while image == None:
        image = pyautogui.locateOnScreen(r"img\worldspan_main.PNG", confidence=0.85)
        time.sleep(5)

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
         
        
# Go to General page
MAX_RETRY_COUNT = 5
WAIT_TIME = 2

def get_element_by_id(driver, element_id):
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )

def refresh_until_text_matches(driver, element_id, target_text, max_retries):
    count = 0
    while count < max_retries:
        try:
            element = get_element_by_id(driver, element_id)
            text = element.text
            time.sleep(WAIT_TIME)
            
            if text == target_text:
                break
            else:
                driver.refresh()
                count += 1
        except TimeoutError as e:
            print(f"TimeoutException: {e}")
            break

def get_general_page():
    driver.get('https://dataweb.accor.net/dotw-trans/displayGeneralInformation!input.action')
    
    try:
        refresh_until_text_matches(driver, 'formTitle', 'General Information', MAX_RETRY_COUNT)
    except Exception as e:
        print(f"An error occurred: {e}")


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
        

# create code
hotel_rid = input('Please Enter Hotel RID: ')
hotel_rid = str(hotel_rid).upper()
file_path = f"gds\worldspan\{hotel_rid} Worldspan.csv"
df = pd.read_csv(file_path, dtype=str)

worldspan_code = df['worldspan code'].iloc[0]

# Setup Chrome Driver
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": r"C:\Users\NSANGKARN\bodytaylor\TARSautomation\temp"}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--headless")  # Enable headless mode
driver = webdriver.Chrome(options=chrome_options)

# Get data
username, password = user_credential()
login(username, password)
hotel_search(hotel_rid=hotel_rid)

get_general_page()

# Update Geo Location
# HHGM + Chain code + worldspand code

# Latitude
latitude = get_data(element_id='gi.coodY')
latitude = float(latitude)
if abs(latitude) < 10:
    latitude_6decimals = "0" + "{:.6f}".format(abs(latitude)) 
else:
    latitude_6decimals = "{:.6f}".format(abs(latitude)) 
    
if latitude > 0:
    latitude_formatted = ' ' + str(latitude_6decimals)
else:
    latitude_formatted = '-' + str(latitude_6decimals)


# Longtitude
longtitude = get_data(element_id='gi.coordX')
longtitude = float(longtitude)
if abs(longtitude) < 100:
    longtitude_6decimals = "0" + "{:.6f}".format(abs(longtitude)) 
else:
    longtitude_6decimals = "{:.6f}".format(abs(longtitude)) 
    
if longtitude > 0:
    longtitude_formatted = ' ' + str(longtitude_6decimals)
else:
    longtitude_formatted = '-' + str(longtitude_6decimals)

# iata code from AER1
surrounding = get_surrounding()
result = surrounding[surrounding['Code'] == 'AER1']
iata_code = result['Name'].values[0]

# Distance in Mile (Round Number) 
distance_m = result['Miles'].values[0]
distance_m = str(int(round(distance_m, 0)))

# Unit always M
unit = 'M'  

# Oppsite direction of AER1 in TARS
orientation = result['Orientation'].values[0]
opp_orientation = find_opposite_dir(direction=orientation)


# Enter Worldspan Geo code
find_gds_windows()
pyautogui.typewrite('HHGM' + worldspan_code)
pyautogui.press('enter')
time.sleep(2)

f.tabing(6)
type_with_delay(latitude_formatted)
f.tabing(1)
type_with_delay(longtitude_formatted)
f.tabing(1)
type_with_delay(iata_code)
f.tabing(2)
type_with_delay(distance_m)
f.tabing(1)
type_with_delay(unit)
f.tabing(1)
type_with_delay(opp_orientation)
f.tabing(4)
time.sleep(2)
save()
time.sleep(1.5)



# ADD Surrounding
c_country = df['CNTRY'].iloc[0]

ctr1 = surrounding[surrounding['Code'] == 'CTR1']
ctr1_name = ctr1['Name'].values[0]
ctr1_dis = ctr1['Miles'].values[0]
ctr1_dis = str(int(round(ctr1_dis)))
ctr1_dir = ctr1['Orientation'].values[0]
ctri_opp_dir = find_opposite_dir(direction=ctr1_dir)

pcn = surrounding[surrounding['Code'] == 'PCN']
pcn_name = pcn['Name'].values[0]
pcn_dis = pcn['Miles'].values[0]
pcn_dis = str(int(round(pcn_dis)))
pcn_dir = pcn['Orientation'].values[0]
pcn_opp_dir = find_opposite_dir(direction=pcn_dir)

apt1 = surrounding[surrounding['Code'] == 'APT1']
apt1_name = apt1['Name'].values[0]
apt1_dis = apt1['Miles'].values[0]
apt1_dis = str(int(round(apt1_dis)))
apt1_dir = apt1['Orientation'].values[0]
apt1_opp_dir = find_opposite_dir(direction=apt1_dir)

pyautogui.typewrite('HHTA' + worldspan_code)
pyautogui.press('enter')
time.sleep(2)
f.tabing(7)

type_with_delay(text=ctr1_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=ctr1_dis)
f.tabing(1)
type_with_delay(text=ctri_opp_dir)
f.tabing(1)

type_with_delay(text=pcn_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=pcn_dis)
f.tabing(1)
type_with_delay(text=pcn_opp_dir)
f.tabing(1)

type_with_delay(text=apt1_name)
f.tabing(2)
type_with_delay(text=c_country)
f.tabing(1)
type_with_delay(text=apt1_dis)
f.tabing(1)
type_with_delay(text=apt1_opp_dir)
f.tabing(1)
f.tabing(31)
save()
time.sleep(1.5)

# guarantee 
pyautogui.typewrite('HHQA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(13)

# Get current time data
current_datetime = datetime.datetime.now()
# Format to DDMMYY
formatted_date = current_datetime.strftime("%d%b%y").upper()

pyautogui.typewrite(formatted_date + '-' + 'XXXXXXX')
f.tabing(1)
pyautogui.typewrite('1234567')
f.tabing(1)
pyautogui.typewrite('1800')
f.tabing(1)
pyautogui.typewrite('X')
f.tabing(43)
pyautogui.press('right', presses=5, interval=0.15)
pyautogui.press('enter')
time.sleep(1)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# canpol
pyautogui.typewrite('HHNA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(15)
time.sleep(0.5)

pyautogui.typewrite(formatted_date + '-' + 'XXXXXXX')
f.tabing(1)
pyautogui.typewrite('1234567')
f.tabing(1)
pyautogui.typewrite('1800')
f.tabing(28)
pyautogui.press('right', presses=10, interval=0.15)
pyautogui.press('enter')
time.sleep(1)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# Amemities add only one the rest will flow
pyautogui.typewrite('HHMA' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)
f.tabing(20)
time.sleep(0.5)
pyautogui.typewrite('X')
f.tabing(1)
pyautogui.press('enter')
time.sleep(1.5)
pyautogui.typewrite('HUE')
pyautogui.press('enter')
time.sleep(1.5)

# Activate Hotel
pyautogui.typewrite('HHWU' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)

# Check unlock status
pyautogui.typewrite('HHWR' + worldspan_code)
pyautogui.press('enter')
time.sleep(1.5)

driver.quit()                


