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
    
hotel_list = ['9778','A545','B682','C2B8','C1P3','C1R2','C1I6',
              'C1P2','C1R1','C1Q8','C1P4','C1P0','C1Q1','C1Q3',
              'C1Q7','C1P6','C1P9','C1Q2','C1Q5','C1P7','C1N8',
              'C1N7','C1P5','C1N6','C1Q6',]
    
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