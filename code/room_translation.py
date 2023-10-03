import time
import pandas as pd
from functions import *

# get room code and store as list
def get_room_data():
    excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Roomtypes"
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols='C, AC, AA', skiprows=9, nrows=15)
    df.columns = ['room_code', 'marketing_label', 'tar_ref']
    df = df.dropna()
    return df

# Confirm Hotel RID and select mode
hotel_rid = input('Enter Hotel RID: ')  
translate_or_update = int(input('Translate Hit: 1 \nUpdate Hit: 2\nPlease type number and Hit Enter: '))

# Get room data from excel sheet
df = get_room_data()
# Check for unaccepted characters, if there are any, script will terminate!
check_text(df, col='marketing_label')
check_text(df, col='tar_ref')

# Start the loop!
for i in range(len(df)):
    # Get room code
    room_code = df.iloc[i, 0]
    
    # Open Web Browser on translate page and wait for webpage load
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelProduct!input.action?actionType=translate&hotelProduct.code={room_code}&hotelProduct.type.code=ROOMSU&hotelProduct.centralUse=true&'
    open_web(url)
    find_logo()
    
    # Click on Translate 
    find_and_click_on('TARSautomation\\img\\translate.png')
    time.sleep(2)
    
    # Click on menu and locate discription input box
    find_and_click_on('TARSautomation\\img\\translate_product.PNG')
    tabing(6)
    
    # Get data from DataFrame and type in the discription box, do not change the secound locater!
    description = df.iloc[i, 2]
    type_translate(2, description)
    
    # Get data from DataFrame and type in the marketing lable, box do not change the secound locater!
    marketing_label = df.iloc[0, 1]
    type_translate(translate_or_update, marketing_label)

    # Select translate or update
    if translate_or_update == 1:
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
    else:
        pyautogui.press('enter')
        time.sleep(1)

    # close browser
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')

if translate_or_update == 1:
    print(f'Translation for all rooms in {hotel_rid} is done!')
else:
    print(f'Discription for all rooms in {hotel_rid} is done! Please comeback and hit translate later!')