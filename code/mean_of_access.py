import time
import pyautogui
import re
from functions import *

def add(hotel_rid):
    url = 'https://dataweb.accor.net/dotw-trans/accessTabs!input.action'
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Address&Setup"
    code_list = []

    open_web(url)           
    load_excel_file(excel_file_path, sheet_name)

    # navigate Accesses library tab
    main_search_box('accm')
    time.sleep(2)
    find_add()
    time.sleep(1)

    # go to the entry form
    find_and_click_on('img\\add_access.PNG')
    tabing(2)

    # Enter Hotel name
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            hotel_name = sheet['C4'].value
            pyautogui.typewrite(hotel_name)
            tabing(4)
            pyautogui.press('enter')
            time.sleep(1)
            
            # add translation
            hotel_direction = sheet['C79'].value
            hotel_name_url = str(hotel_name).replace(" ", "+")
            url_translation = f'https://dataweb.accor.net/dotw-trans/translateHotelAccess!input.action?actionType=translate&hotelAccess.accessType.code=ACCM&hotelAccess.name={hotel_name_url}&'
            open_web(url_translation)
            
            # Click on translation button
            find_and_click_on('img\\translate.png')
            find_logo()
            
            # Locate a input section
            find_and_click_on('img\\translate_menu.PNG')
            tabing(8)
            time.sleep(1)
            
            # Input Translation
            type_translate(1, message=hotel_direction)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            
            # Wait and close tab
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1)
            
            # Add another attraction
            for i in range(4):
                if sheet[f'E{144 + i}'].value != None:
                    pattern = r'([A-Z]+) -'
                    code = re.findall(pattern, sheet[f'C{149 + i}'].value)[0]
                    code_list.append(code)
                    data = [sheet[f'E{144 + i}'].value,
                            sheet[f'H{144 + i}'].value,
                            sheet[f'I{144 + i}'].value,
                            sheet[f'K{144 + i}'].value]
                    main_search_box(code)
                    time.sleep(1)
                    find_add()
                    time.sleep(1)
                    find_and_click_on('img\\add_access.PNG')
                    tabing(2)
                    enter_data(data)
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close()
            
    print(f'Mean of Access has been added to {hotel_rid}!')
    print('Next Step Add Surrounding Attractions')
    

