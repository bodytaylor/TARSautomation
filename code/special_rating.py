import time
import TarsAutomation as ta

def add(hotel_rid, hotel_content):
    
    local_rating = hotel_content.local_rating
    north_star = hotel_content.north_star

    # walk to this url
    ta.get("https://dataweb.accor.net/dotw-trans/displayHotelStandings!input.action")
    ta.wait_for_element(element="allStandingsTabLink")

    # At Local Star Rating
    ta.driver.execute_script("addBasicElement('EU','Local star rating','Star');")
    ta.wait_for_element(element="actionTypeTitle")
    ta.input_text(element_id="hotelStanding.nb", text=local_rating)
    time.sleep(0.5)
    ta.driver.execute_script("if(validateForm_hotelStandingForm()){oHotelStanding.majHotelElement('add');}")
    ta.get_response(hotel_rid, code='hotelStanding')
    
    # Add North star rating
    if north_star is not None:
        ta.driver.execute_script("addBasicElement('OH','Northstar Travel Media','');return true;")
        ta.wait_for_element(element="actionTypeTitle")
        ta.input_text(element_id='hotelStanding.nb', text=north_star)
        time.sleep(0.5)
        ta.driver.execute_script("if(validateForm_hotelStandingForm()){oHotelStanding.majHotelElement('add');}")
        ta.get_response(hotel_rid, code='hotelStanding')
        
    ta.logger.info(f'Automation Add Rating Done')