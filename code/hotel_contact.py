from functions import *
from dictionary import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *
import time


# execute java script
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
    
# Name ACCOR Standard check
def accor_name(title, input_name, input_surname) -> str:
    name = input_name[0].upper() + input_name[1:].lower()
    surname = input_surname.upper()
    return f'{title} {name} {surname}'

# Name ACCOR Standard for single cell
def accor_format_name(title, text_input) -> str:
    if text_input and title is not None:
        words = text_input.split()
        formatted_name = words[0].capitalize()
        for word in words[1:]:
            formatted_name += " " + word.upper()
        title = title.replace(".", "")
        return f'{title} {formatted_name}'
    else:
        return None
    
def add(hotel_rid):
    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    gm_data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['E53', 'J55', 'J53'], 
        sheet_name='Address&Setup'
    )

    # GM name
    gm = accor_name(gm_data[0], gm_data[1], gm_data[2])

    # Create Contact list of elements and input value
    contact_dict ={
        "hotelContactsForm_hotelStaffManagers_generalManager_name": gm,
    }

    # walk to this url
    driver.get("https://dataweb.accor.net/dotw-trans/displayHotelContacts.action")
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelContactsTabs"]'))
        )

    ## input text data ##
    for key, value in contact_dict.items():
        input_text(element_id=key, text=value)

    print('Automation Done Please Review The input data before click save! Thanks.')