from dictionary import *
import TarsAutomation as ta

def add(hotel_rid):
    # Goto Target URL
    ta.get("https://dataweb.accor.net/dotw-trans/secure/displayHotelPayments.action")
    ta.wait_for_element('paymentsTabs')

    # Let Rolls!
    payment_list = ['AX', 'CA', 'VI', 'WIRE', 'CREDIT', 'PCHECK', 'CR', 'CCHECK', 'PREPA1', 'PRCARD']
    for item in payment_list:
        ta.add_element(item)
        if item not in ['CCHECK', 'PREPA1', 'PRCARD']:
            ta.tick_box('hotelPaymentForm_hotelPayment_availableOnGdsOrMedias')
        ta.click_button('addButton')
        ta.get_response(hotel_rid, code=item)
        