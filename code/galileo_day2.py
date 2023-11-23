import pyautogui
import time
import functions as f

# find console
def find_gds_windows():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\roomaster.PNG", confidence=0.85)
    print('Please Open GDS - Term Roommaster')
    while image == None:
        image = pyautogui.locateOnScreen(r"img\roomaster.PNG", confidence=0.85)
        time.sleep(5)
        
# type rms and enter
# get login credential

# enter username and password for selected chian
# tab 1 time for enter chain code
# select 1 for master data
# select 1 for entering property data

# Entering data
f.tabing(8)

# Country
f.tabing(2)

# zip code
f.tabing(1)

# Phone Number
f.tabing(4)

# Fax Number if available
f.tabing(1)
pyautogui.press('enter')
time.sleep(2)

# Go go 2nd page
pyautogui.press('f8')
time.sleep(2)
f.tabing(6)

# Property type




