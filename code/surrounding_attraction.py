import TarsAutomation as ta
import re
from dictionary import surrouding_dict

def extract_capital_letters(input_string):
    # Define the regular expression pattern to match capital letters
    pattern = r'[A-Z]'
    matches = re.findall(pattern, input_string)
    capital_letters = ''.join(matches)
    return capital_letters
       
# for data enter in add attraction page
def enter_from_df(df, catagory: str, check_exist: list, unit_select: str, hotel_rid):
    for index, row in df.iterrows():
        if row['name'] not in check_exist:
            code = catagory
            if str(row['orientation']) != 'nan':
                ofi = extract_capital_letters(row['orientation'])
            else:
                ofi = 0
            shuttle = row['shuttle']
            shuttle_service_type = row['shuttle_service']
            distance = row['distance']
            minute_walk = row['time_walk']
            minute_drive = row['time_drive']
            
            # Add
            code_name = surrouding_dict.get(code)
            ta.driver.execute_script(f"addBasicElement('{code}','{code_name}');")
            ta.wait_for_element('formTitle')
            
            # Name
            ta.input_text(element_id='hotelIp.name', text=row['name'])
                            
            # Shuttle service
            if ((shuttle == 'Yes free') or (shuttle == 'Yes paying')): # Tick on Shuttle
                ta.driver.execute_script('var checkbox = document.getElementById("hotelIp.shuttle"); checkbox.checked = !checkbox.checked; changeShuttleValue();')
                if shuttle_service_type == 'On call':
                    ta.tick_box(element='hotelIp.shuttle.onCall')

                if shuttle_service_type == 'Scheduled':
                    ta.tick_box(element='hotelIp.shuttle.scheduled')
                            
                if shuttle == 'Yes free':
                    ta.tick_box(element='hotelIp.shuttle.free')
                                    
            # Distance 
            if str(distance) != 'nan':
                ta.driver.execute_script(f'var DistanceInput = document.getElementById("{unit_select}"); DistanceInput.value = "{distance}"; (document.createEventObject ? DistanceInput.fireEvent("onchange", document.createEventObject()) : DistanceInput.dispatchEvent(new Event("change")));')
       
            # Minute Walk
            if str(minute_walk) == 'nan':
                ta.input_text(element_id='hotelIp.walkingTime', text='99')
            else:
                ta.input_text(element_id='hotelIp.walkingTime', text=str(minute_walk))
                            
            # Minite Drive
            if str(minute_drive) == 'nan':
                pass
            else:
                ta.input_text(element_id='hotelIp.carTime', text=str(minute_drive))
                            
            # Orientation to the hotel
            if ofi != 0:
                ta.select_dropdown(element_id='hotelIp.orientation', value=str(ofi))
                            
            # Always Tick on Available on GDS and Media
            ta.tick_box(element='hotelIp.availableOnGdsMedia')
                            
            # Click Add
            ta.driver.execute_script('submitFormIp();')
            
            # Get response
            ta.get_response(hotel_rid, code=row['name'])
                            
def add(hotel_rid, hotel_content):
    main_attractions = []
    for key in hotel_content.main_attractions:
        main_attractions.append(hotel_content.main_attractions[key][0][0])
    unit_select = hotel_content.unit_select
    
    # set web target
    url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
    # open target url
    ta.get(url)
    ta.wait_for_element('allIpsTabLink')
    
    # Enter Data for 4 df
    enter_from_df(hotel_content.comp, catagory='COMP', check_exist=main_attractions, unit_select=unit_select, hotel_rid=hotel_rid)
    enter_from_df(hotel_content.cong, catagory='CONG', check_exist=main_attractions, unit_select=unit_select, hotel_rid=hotel_rid)
    enter_from_df(hotel_content.exhi, catagory='EXHI', check_exist=main_attractions, unit_select=unit_select, hotel_rid=hotel_rid)
    enter_from_df(hotel_content.expo, catagory='EXPO', check_exist=main_attractions, unit_select=unit_select, hotel_rid=hotel_rid)   
