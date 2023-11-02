import time
import pyautogui
from functions import *
from dictionary import *

# input textbox
def input_text(element_id, text):
    pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    
def add(hotel_rid):
    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['D32', 'C39', 'C34', 'J34', 'C37'], 
        sheet_name='Address&Setup'
    )

    # Create Elements Dict
    elements_dict = {}

    elements_dict['hotelDataTranslate.translatedCommercialName'] = data[0]
    elements_dict['hotelDataTranslate.translatedCity'] = data[1]
    elements_dict['hotelDataTranslate.translatedAddress1'] = data[2]
    elements_dict['hotelDataTranslate.translatedAddress2'] = data[3]
    elements_dict['hotelDataTranslate.translatedAddress3'] = data[4]

    # Tell user to open web console
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/displayHotelData!input.action')
    time.sleep(2)

    # Click on Translation Langauge GB
    translate_button = "var elements = document.getElementsByClassName('zoneCliquable'); if (elements.length > 0) { elements[0].click(); }"
    type_and_enter(translate_button)
    time.sleep(2)

    switch_mode()
    # Start Writing in the browser console
    for key, value in elements_dict.items():
        if value != None:
            input_textf(key, value)
            
    switch_mode()
    pyautogui.press('enter')
    time.sleep(1)
    # Click translate and confirm
    type_and_enter(text='document.getElementById(\"hotelDataForm.submitButton\").click();')
    time.sleep(1)
    pyautogui.press('enter')

    print('Translate Name and Address Done!')