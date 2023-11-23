import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *
from dictionary import *
        
# input textbox
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)
    
    
def add(hotel_rid):
    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['D32', 'C39', 'C34', 'J34', 'C37', 'K10'], 
        sheet_name='Address&Setup'
    )
    
    # Hotel Commercial Name D32
    hotel_com_name = data[0]

    # Provisional Opening date merge with commercial name K10
    open_date = data[5]
    open_date = open_date.strftime("%B %Y")
    hotel_com_name = f'{hotel_com_name} (Opening {open_date})'

    # Create Elements Dict
    elements_dict = {}

    elements_dict['hotelDataTranslate.translatedCommercialName'] = hotel_com_name
    elements_dict['hotelDataTranslate.translatedCity'] = data[1]
    elements_dict['hotelDataTranslate.translatedAddress1'] = data[2]
    elements_dict['hotelDataTranslate.translatedAddress2'] = data[3]
    elements_dict['hotelDataTranslate.translatedAddress3'] = data[4]

    # Tell user to open web console

    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelData!input.action')
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="transHotelTabLink"]'))
        )
    print(f'[INFO] - {page.text}')

    # Click on Translation Langauge GB
    translate_button = "var elements = document.getElementsByClassName('zoneCliquable'); if (elements.length > 0) { elements[0].click(); }"
    driver.execute_script(translate_button)
    time.sleep(2)

    # Start Writing in the browser console
    for key, value in elements_dict.items():
        if value != None:
            input_text(element_id=key, text=value)
            
    time.sleep(1)
    # Click translate and confirm
    driver.execute_script('document.getElementById(\"hotelDataForm.submitButton\").click();')
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()

    print('Translate Name and Address Done!')