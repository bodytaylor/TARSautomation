import TarsAutomation as ta
from selenium.webdriver.common.by import By

def add(hotel_rid, hotel_content):
    df = hotel_content.room_description_df
    translate_or_update = int(input('Translate Hit: 1 \nUpdate Hit: 2\nPlease type number and Hit Enter: '))

    # Start the loop!
    for i in range(len(df)):
        # Get room code
        room_code = df.iloc[i, 0]
        room_type = find_type(df=hotel_content.product_lib_df, code=room_code)
        
        # Open Web Browser on translate page and wait for webpage load
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={room_code}&hotelProduct.type.code={room_type}&hotelProduct.centralUse=true&'
        ta.get(url)
        ta.wait_for_element(element='zoneCliquable', by=By.CLASS_NAME)

        # Click on Translate 
        ta.driver.execute_script(f"displayTranslateForm('translateInput','GB','{room_code}','{room_type}','{hotel_rid}','productsDescriptionsTable','true','true','GB','true')")
        
        # Wait for page to load
        ta.wait_for_element(element='translateHotelProductFormJson')
    
        # find description box
        description_box = ta.driver.find_element(By.ID, "hotelProductTranslate.description")
        marketing_box =  ta.driver.find_element(By.ID, "hotelProductTranslate.referenceLabel")
        
        # Clear the box
        ta.driver.execute_script("document.getElementById('hotelProductTranslate.description').value = '';")
        ta.driver.execute_script("document.getElementById('hotelProductTranslate.referenceLabel').value = '';")
            
        # Get data from DataFrame and type in the discription box, do not change the secound locater!
        description = df.iloc[i, 2]
        description_box.send_keys(description)
            
        # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
        marketing_label = df.iloc[i, 1]
        marketing_box.send_keys(marketing_label)

        # Select translate or update
        ta.translate_hotel_product(translate_or_update)
            
        # get response
        ta.get_response(hotel_rid, code=room_code)
    
    ta.logger.info(f'{hotel_rid} : Room Translation Complete')