import time
from TarsAutomation import driver, logger
import TarsAutomation as ta
from dictionary import *
    
def add(hotel_rid, hotel_content):
    
    # Hotel Commercial Name D32
    hotel_com_name = hotel_content.hotel_com_name

    # Provisional Opening date merge with commercial name K10
    open_date = hotel_content.open_date
    open_date = open_date.strftime("%B %Y")
    hotel_com_name = f'{hotel_com_name} (Opening {open_date})'

    # Create Elements Dict
    elements_dict = {}

    elements_dict['hotelDataTranslate.translatedCommercialName'] = hotel_com_name
    elements_dict['hotelDataTranslate.translatedCity'] = hotel_content.city
    elements_dict['hotelDataTranslate.translatedAddress1'] = hotel_content.address1
    elements_dict['hotelDataTranslate.translatedAddress2'] = hotel_content.address2
    elements_dict['hotelDataTranslate.translatedAddress3'] = hotel_content.address3

 
    # Go to Translate name and Address page
    ta.get('https://dataweb.accor.net/dotw-trans/displayHotelData!input.action')
    
    # Click on Translation Langauge GB
    translate_button = "var elements = document.getElementsByClassName('zoneCliquable'); if (elements.length > 0) { elements[0].click(); }"
    driver.execute_script(translate_button)
    time.sleep(2)

    # Start Writing in the browser console
    for key, value in elements_dict.items():
        if value != None:
            ta.input_text(element_id=key, text=value)
            
    time.sleep(1)
    
    # Click translate and confirm
    driver.execute_script('document.getElementById(\"hotelDataForm.submitButton\").click();')
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    ta.get_response(hotel_rid, code='Display Name')

    print('Translate Name and Address Done!')