import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.15)
    
# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.15)

def click_button(element):
    pyautogui.typewrite(f'document.getElementById("{element}").click();')
    time.sleep(0.25)

def add(hotel_rid):
    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['C79', 'J79'], 
        sheet_name='Address&Setup'
    )

    local_rating = data[0]
    north_star = data[1]

    # walk to this url
    driver.get("https://dataweb.accor.net/dotw-trans/displayHotelStandings!input.action")
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="allStandingsTabLink"]'))
        )
    print(f'[INFO] - {page.text}')
    # input data
    # Click Add
    driver.execute_script("addBasicElement('EU','Local star rating','Star');")
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionTypeTitle"]'))
        )
    time.sleep(1)
    input_text(element_id="hotelStanding.nb", text=local_rating)
    time.sleep(0.5)
    driver.execute_script("if(validateForm_hotelStandingForm()){oHotelStanding.majHotelElement('add');}")
    time.sleep(1.5)
    
    # north star rating
    if north_star != None:
        driver.execute_script("addBasicElement('OH','Northstar Travel Media','');return true;")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionTypeTitle"]'))
        )
        time.sleep(1)
        input_text(element_id='hotelStanding.nb', text=north_star)
        time.sleep(0.5)
        driver.execute_script("if(validateForm_hotelStandingForm()){oHotelStanding.majHotelElement('add');}")
    
    print(f'[INFO] - Automation Aadd Rating Done')