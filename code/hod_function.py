import time
import pyautogui
from functions import *


# Find web browser console
def page_load(img):
    time.sleep(1)
    image = pyautogui.locateOnScreen(img, confidence=0.8)
    while image == None:
        image = pyautogui.locateOnScreen(img, confidence=0.8)
        time.sleep(2)
        print('waiting for page to load')
    time.sleep(1)
    
def enter_bed_num(i, bed_num):
    type_and_enter(f"""var targetIndex = {i};
var inputElements = document.querySelectorAll('input[type="number"][ng-model="innerValue"]');
var inputElement = inputElements[targetIndex];
var newValue = {bed_num};
inputElement.value = newValue;
var event = new Event('change', {{ bubbles: true }});
inputElement.dispatchEvent(event);""")
    

