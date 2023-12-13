import TarsAutomation as ta
import time
        
# Mean Of Access dict
mean_of_acces_dict = {
    'RER': 'By RER',
    'BUSS': 'By bus',
    'AUT1': 'By car',
    'AUT2': 'By car',
    'AUTO': 'By car',
    'CARE': 'By car from the east',
    'CARN': 'By car from the north',
    'CARS': 'By car from the south',
    'CARW': 'By car from the west',
    'FERR': 'By ferry',
    'CBUS': 'By free shuttle/courtesy bus',
    'PORT': 'By harbour',
    'HELI': 'By helicopter',
    'LIMO': 'By limousine',
    'MOTR': 'By motorway',
    'MOTE': 'By motorway from the east',
    'MOTN': 'By motorway from the north',
    'MOTS': 'By motorway from the south',
    'MOTW': 'By motorway from the west',
    'AERO': 'By plane',
    'AIR1': 'By plane',
    'RAIL': 'By railway',
    'ROUT': 'By road',
    'METR': 'By subway',
    'TAXI': 'By taxi',
    'TRAM': 'By tram',
    'ACCM': 'Means of access',
    'WALK': 'On foot',
    'PBUS': 'Paying Shuttle',
    }

# Function for entering data in Tars Mean of Access
def enter_data(data):
    element_list = [
        'hotelAccess.name', 'hotelAccess.direction', 'hotelAccess.line', 'hotelAccess.station'
    ]
    # Loop through the data and enter it
    for i, value in enumerate(data):
        if value != None:
            ta.input_text(element_id=element_list[i], text=value)

def add(hotel_rid, hotel_content):
    # Open Webpage
    url = 'https://dataweb.accor.net/dotw-trans/accessTabs!input.action'
    ta.get(url)
    ta.wait_for_element('hotelAccessesTable')
    
    # add
    ta.driver.execute_script("addBasicElement('ACCM','Means of access');")
    ta.wait_for_element('hotelAccessFormDiv')
    
    hotel_name = hotel_content.hotel_name
    ta.input_text(element_id='hotelAccess.name', text=hotel_name)
    ta.driver.execute_script("submitFormAccess();")
    time.sleep(2)
    
    # add translation 
    hotel_direction = hotel_content.hotel_direction         
    hotel_name_url = str(hotel_name).replace(" ", "+")
    url_translation = f'https://dataweb.accor.net/dotw-trans/translateHotelAccess!input.action?actionType=translate&hotelAccess.accessType.code=ACCM&hotelAccess.name={hotel_name_url}&'
    ta.get(url_translation)
    ta.wait_for_element('accessesDescriptionsTable')

    # Add
    ta.driver.execute_script(f"displayTranslateForm('translateInput','GB','ACCM','accessesDescriptionsTable','true','true','GB','true');")
    time.sleep(1)
    
    # Input Translation
    ta.input_text(element_id='hotelAccessTranslate.translatedDescription', text=hotel_direction)
    
    # Click on Translate button
    ta.translate_hotel_product(element_id='translateHotelAccessForm')
    
    # get response
    ta.get_response(hotel_rid, code='ACCM')
 
    # Add another attraction
    # Open Webpage
    url = 'https://dataweb.accor.net/dotw-trans/accessTabs!input.action'
    ta.get(url)
    ta.wait_for_element('hotelAccessesTable')
    mean_of_access_data = hotel_content.mean_of_access
    for key in mean_of_access_data:
        code = str(key).strip()
        data = mean_of_access_data[key]
        acc_name = mean_of_acces_dict.get(code)
        
        # Add surrounding
        ta.driver.execute_script(f"addBasicElement('{code}','{acc_name}');")
        
        # Wait for the form to appear
        ta.wait_for_element('formTitle')
        enter_data(data)
        
        # Click add
        ta.driver.execute_script("submitFormAccess();")
        
        # Print the response
        ta.get_response(hotel_rid, code)
        
        