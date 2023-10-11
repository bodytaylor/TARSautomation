from datetime import datetime
from functions import *
from dictionary import *


# input textbox
def input_text(element_id, text):
    if text != None:
        pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.5)
        pyautogui.press('enter')
        
# Click Add
def add_element(element):
    pyautogui.typewrite(f"addBasicElement('{element}');")
    pyautogui.press('enter')
    time.sleep(0.5)

# tick box
def tick_box_select(element_id):
    pyautogui.typewrite(f'document.getElementById("{element_id}").checked = true;')
    pyautogui.press('enter')
    time.sleep(0.5)
    
# Click on
def click_on_element(element_id):
    pyautogui.typewrite(f'document.getElementById("{element_id}").click();')
    pyautogui.press('enter')
    time.sleep(0.5)

    
# Ask user for RID    
hotel_rid = str(input('Enter Hotel RID: '))
# Make it All Cap
hotel_rid = hotel_rid.upper()

# Tell user to open web console
find_edge_console()

# Fill data in console
# Goto Target URL
type_and_enter(text='window.location.href = "https://dataweb.accor.net/dotw-trans/secure/displayHotelPayments.action";')
time.sleep(2.5)
find_logo()
# clear console
pyautogui.hotkey('ctrl', 'l')

# Let Rolls!
payment_list = ['AX', 'CA', 'VI', 'WIRE', 'CREDIT', 'PCHECK', 'CR', 'CCHECK', 'PREPA1', 'PRCARD']
for item in payment_list:
    add_element(item)
    if item not in ['CCHECK', 'PREPA1', 'PRCARD']:
        tick_box_select('hotelPaymentForm_hotelPayment_availableOnGdsOrMedias')
    click_on_element('addButton')
    time.sleep(1)
    
print('Happy Looping')