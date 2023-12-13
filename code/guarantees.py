
from dictionary import *
import TarsAutomation as ta

def add(hotel_rid):
    # Goto Target URL
    ta.get("https://dataweb.accor.net/dotw-trans/secure/guaranteeTabs!input.action")
    ta.wait_for_element('allGuaranteesTabLink')

    # Let Rolls!
    guarantees_list = ['AX','CA', 'VI', 'WIRE', 'IATA', 'PCHECK', 'CASH', 'CCHECK', 'PREP1', 'GTO']
    for item in guarantees_list:
        ta.add_element(item)
        if item == 'IATA':
            ta.tick_box('hotelGuarantee.qualified')
        if item not in ['PCHECK', 'CCHECK']:
            ta.tick_box('hotelGuarantee.availableOnGDSMedia')
        ta.click_button('hotelGuarantee.submitButton')
        ta.get_response(hotel_rid, code=item)
        
        