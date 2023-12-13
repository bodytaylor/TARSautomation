import TarsAutomation as ta
from selenium.webdriver.common.by import By

def add(hotel_rid, hotel_content):
    bars = hotel_content.bars
    # Start Looping!
    for keys in bars:
        # find type
        bar_code = bars[f'{keys}'][0]['Code']
        description = bars[f'{keys}'][7]['Description']
        key = keys.upper()
        key = ta.url_parse(key)
        # Open webbrowser
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelBar!input.action?actionType=translate&hotelBar.barType.code={bar_code}&hotelBar.name={key}&'
        ta.get(url)
        # Wait for page to load
        ta.wait_for_element('barsDescriptionsTable')
        
        # Click on Translate 
        ta.driver.execute_script(f"displayTranslateForm('translateInput','GB','{bar_code}','barsDescriptionsTable','true','true','GB','true');")
        
        # wait for form to appear
        ta.wait_for_element('translateHotelBarFormJson')
    
        # find description box
        description_box = ta.driver.find_element(By.ID, "hotelBarTranslate.description")
        description_box.send_keys(description)
        
        ta.translate_hotel_product(element_id='translateHotelBarForm')
            
        # get response
        ta.get_response(hotel_rid, code=bar_code)
