import time
import pyautogui
from functions import *

hotel_rid = input('Enter Hotel RID: ')
hotel_rid = str(hotel_rid).upper()

# insert function
def type_and_enter(text):
    text = str(text)
    pyautogui.typewrite(text)
    time.sleep(0.5)
    pyautogui.press('enter')

# Open target web
webbrowser.open('https://dataweb.accor.net/dotw-trans/displayHotelAutomation!input.action')
find_logo()
# open browser console
pyautogui.hotkey('win', 'r')
time.sleep(1)
pyautogui.typewrite(r"%systemroot%\system32\f12\IEChooser.exe")
time.sleep(1)

pyautogui.press('enter')
time.sleep(2)
tabing(3)
pyautogui.press('enter')
# wait for webpage to load
find_logo()
time.sleep(5)
pyautogui.hotkey('ctrl', '2')
time.sleep(1)
find_and_click(img_path=r'img\ie12.PNG')

# ready to roll!!
automation_list = ['RT', 'DQ', 'GG', 'HO', 'TE']

for item in automation_list:
    find_logo()
    # pass value to type
    add = 'addGDSElement();'
    code = f'var inputElement = document.getElementById("system.systemCode"); inputElement.value = "{item}";'
    search = 'searchGDS();'
    hrid = f'var inputElement = document.getElementById("externalCode"); inputElement.value = "{hotel_rid}";'
    save = 'addHotelGDS();'
    
    order = [add, code, search, hrid, save]
    for i in order:
        type_and_enter(i)
        time.sleep(1)
        
    
# for DHISCO

add = 'addGDSElement();'
code = 'var inputElement = document.getElementById("system.systemCode"); inputElement.value = "WB";'
search = 'searchGDS();'
insert = 'var inputElement = document.getElementById("associatedSystList"); inputElement.value = "WB";'
hrid = f'var inputElement = document.getElementById("externalCode"); inputElement.value = "{hotel_rid}";'
save = 'addHotelGDS();'

order = [add, code, search, insert, hrid, save]
for i in order:
    type_and_enter(i)
    time.sleep(1)

print(f'ALL MANDATORY AUTOMATION SYSTEMS HAS BEEN ADDED TO {hotel_rid}')