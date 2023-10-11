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
print('Open web browser console by pressing CTRL + SHIFT + J')
find_console()

# Fill data in console
# Goto Target URL
type_and_enter(text='window.location.href = "https://dataweb.accor.net/dotw-trans/secure/guaranteeTabs!input.action";')
time.sleep(2)
find_logo()

# Let Rolls!
guarantees_list = ['AX','CA', 'VI', 'WIRE', 'IATA', 'PCHECK', 'CASH', 'CCHECK', 'PREP1']
for item in guarantees_list:
    add_element(item)
    if item == 'IATA':
        tick_box_select('hotelGuarantee.qualified')
    if item not in ['PCHECK', 'CCHECK']:
        tick_box_select('hotelGuarantee.availableOnGDSMedia')
    click_on_element('hotelGuarantee.submitButton')
    time.sleep(1)
    
print('Happy Looping')