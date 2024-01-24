from selenium.webdriver.common.by import By
import TarsAutomation as ta
import time

# function for input description into translation page
def enter_description(keys, search_key, description):
    # Open new tab and locate menu
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelLoungeInput.action?actionType=translate&description.lounge.type.code=MEET&description.lounge.name={search_key}'
    ta.driver.get(url)
    ta.wait_for_element(element='zoneCliquable', by=By.CLASS_NAME)
    
    # Click on the element
    ta.driver.execute_script("displayTranslateForm('GB','MEET','true','true','GB','true');")
    time.sleep(1)
        
    # Enter Translations
    textarea = ta.driver.find_element(By.ID, "hotelLoungeTranslation.description.text")
    textarea.send_keys(description)
    time.sleep(1)

    ta.translate_hotel_product(element_id='translateHotelLoungeForm')

def add(hotel_rid, hotel_content):
    meeting_room = hotel_content
        # If all pass, Add translation
    for key in meeting_room:
        description = meeting_room[key][2]
        key = str(key).strip()
        search_key = ta.url_parse(key)
        enter_description(key, search_key, description)
        ta.get_response(hotel_rid, code=key)
        