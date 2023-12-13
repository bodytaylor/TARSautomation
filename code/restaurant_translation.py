import TarsAutomation as ta
from selenium.webdriver.common.by import By

def add(hotel_rid, hotel_content):
    df = hotel_content
        
    # Start looping!
    for i in range(len(df)):
        rt_name = df.iloc[i, 0]
        search_key = rt_name.upper()
        search_key = ta.url_parse(search_key)

        # Open webbrowser
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelRestaurant!input.action?actionType=translate&hotelRestaurant.type.code=RT&hotelRestaurant.name={search_key}&hotelRestaurant.codeRest=R00{i + 1}&'

        ta.get(url)
        # Wait for page to load
        ta.wait_for_element('restaurantsDescriptionsTable')

        # Click on Translate 
        ta.driver.execute_script(f"displayTranslateForm('translateInput','GB','RT','restaurantsDescriptionsTable','true','true','GB','true');")
        
        # wait for form to appear
        ta.wait_for_element('translateHotelRestaurantFormJson')
        
        # find description box
        description_box = ta.driver.find_element(By.ID, "hotelRestaurantTranslate.description")
        
        # Get data from DataFrame and type in the discription box, do not change the secound locater!
        description = df.iloc[i, 1]
        description_box.send_keys(description)
        
        # Click translate
        ta.translate_hotel_product(element_id='translateHotelRestaurantForm')
            
        # get response
        ta.get_response(hotel_rid, code='RT')
        
