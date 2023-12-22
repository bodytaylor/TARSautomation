import pyautogui as pa
from functions import *

def find_dbm():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\\hod_push.PNG", confidence=0.8)
    print('Please Open HOD Push Page')
    while image == None:
        image = pyautogui.locateOnScreen(r"img\\hod_push.PNG", confidence=0.8)
        time.sleep(2)
        
    time.sleep(1)
    
def find_inputbox():
    x, y = pyautogui.locateCenterOnScreen(r'img\\send.PNG', confidence=0.8)
    pyautogui.moveTo(x - 50, y, 0.1)
    pyautogui.click()
    
hotel_list = input('Enter Hotel RID (sperate by space): ').split()
    
find_dbm()

for hotel in hotel_list:
    image = pyautogui.locateOnScreen(r"img\success_push.PNG", confidence=0.8)
    while image == None:
        find_inputbox()
        pa.hotkey('ctrl', 'a')
        time.sleep(1)
        pa.typewrite(hotel)
        find_and_click(img_path=r"img\\send.PNG")
        time.sleep(1)
        pa.press('enter')
        image = pyautogui.locateOnScreen(r"img\success_push.PNG", confidence=0.8)
    find_and_click(img_path=r"img\hod_push.PNG")
    time.sleep(1)