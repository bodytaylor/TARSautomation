import TarsAutomation as ta

def add(hotel_rid, hotel_content):
    # Create Contact list of elements and input value
    contact_dict ={
        "hotelContactsForm_hotelStaffManagers_generalManager_name": hotel_content.gm,
    }

    # walk to this url
    ta.get("https://dataweb.accor.net/dotw-trans/displayHotelContacts.action")
    ta.wait_for_element('hotelContactsTabs')
    
    ## input text data ##
    for key, value in contact_dict.items():
        ta.input_text(element_id=key, text=value)

    ta.driver.execute_script("createHotelContacts();")
    ta.get_response(hotel_rid, code='createHotelContacts')