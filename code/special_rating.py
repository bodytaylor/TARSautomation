import time
import pyautogui
from functions import *

# Ask user for RID    
hotel_rid = str(input('Enter Hotel RID: '))
# Make it All Cap
hotel_rid = hotel_rid.upper()

# get data from excel file
excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

data = get_excel_values(
    file_path=excel_file, 
    cell_addresses=['C79'], 
    sheet_name='Address&Setup'
)

local_rating = data[0]

# Tell user to open web console
print('Open web browser console by pressing CTRL + SHIFT + I')
find_console()

# Fill data in console
# Goto Target URL
type_and_enter(text='window.location.href = "https://dataweb.accor.net/dotw-trans/displayHotelStandings!input.action";')
time.sleep(2)
find_logo()

# input data in console
# Click Add
pyautogui.typewrite("addBasicElement('EU','Local star rating','Star');")
pyautogui.press('enter')
time.sleep(1)
input_text(element_id="hotelStanding.nb", text=local_rating)
click_button('maj')

print(f'Local Star: {local_rating} Added to {hotel_rid}!')