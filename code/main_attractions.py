import time
import pyautogui
import re
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Main Attractions"
open_web(url)
load_excel_file(excel_file_path, sheet_name)

choice_list = [
    'ADMI', 'ENT', 'APAR', 'AQU', 'ARTC', 'PLGA', 'BOT', 'EVNT', 'CAS', 'CINE', 
    'CLIN', 'COLL', 'COMP', 'CONC', 'CONG', 'CULT', 'EMBA', 'ENTE', 'ENTC', 'EVNS',
    'EXHI', 'EXPO', 'GOLF', 'HIST', 'HOPI', 'INDU', 'LAKE', 'MALL', 'MILI', 'MOVI',
    'MUSM', 'TSP', 'OPE', 'OATT', 'OTBU', 'RELI', 'CTR1', 'RAC', 'REST', 'SCHO',
    'SHOM', 'PIST', 'DIVE', 'TOUR', 'CSPO', 'SPOR', 'STAD', 'ATOU', 'INFO', 'WORL',
    'ZOO', 'PZOO'
]

# Extract Capital Letter
def extract_capital_letters(input_string):
    # Define the regular expression pattern to match capital letters
    pattern = r'[A-Z]'
    
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)
    
    # Convert the matches to a string
    capital_letters = ''.join(matches)
    
    return capital_letters

# Loop Start Here!
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Loop over data file
        cell_start = 11
        # Check Unit Select
        if sheet['E8'].value == 'Km':
            unit_select = 2
        else:
            unit_select = 1
        
        for i in range(18):
            if sheet[f'C{cell_start + i}'].value != None:
                # regex for extract text
                pattern = r'([^:]+):'
                extract_cap = r'[A-Z]'
                
                # data from excel
                code = re.findall(pattern, sheet[f'B{cell_start + i}'].value)[0]
                if sheet[f'G{cell_start + i}'].value != None:
                    ofi = extract_capital_letters(sheet[f'G{cell_start + i}'].value)
                else:
                    ofi = 0
                shuttle = str(sheet[f'D{cell_start + i}'].value)
                shuttle_service_type = str(sheet[f'E{cell_start + i}'].value)
                distance = (sheet[f'I{cell_start + i}'].value)
                minute_walk = (sheet[f'J{cell_start + i}'].value)
                minute_drive = (sheet[f'K{cell_start + i}'].value)
                
                if code in choice_list:
                    choice = 2
                    action_description = 'Leisure and Business'
                else:
                    choice = 1
                    action_description = 'Locations'

                search_with_choice(code, choice=choice)
                find_add()
                time.sleep(1)
                tabing(6)
                print(f'Select {action_description}')

                # Name
                pyautogui.write(sheet[f'C{cell_start + i}'].value)
                
                # Shuttle service
                tabing(1)
                if ((shuttle == 'Yes free') or (shuttle == 'Yes paying')): # Tick on Shuttle
                    pyautogui.press('space')
                    tabing(1)
                    if shuttle_service_type == 'On call':
                        pyautogui.press('space')
                        tabing(1)
                    else:
                        tabing(1)

                    if shuttle_service_type == 'Scheduled':
                        pyautogui.press('space')
                        tabing(1)
                    else:
                        tabing(1)
                        
                    if shuttle == 'Yes free':
                        pyautogui.press('space')
                    else:
                        tabing(1)
                        
                # Distance 
                tabing(2 + unit_select)
                if distance != None:
                    pyautogui.write(str(distance))
                    tabing(1)
                else:
                    tabing(1)
                
                # Minute Walk
                if minute_walk == None:
                    pyautogui.write('99')
                else:
                    pyautogui.write(str(minute_walk))
                tabing(1)
                
                # Minite Drive
                if minute_drive == None:
                    tabing(1)
                else:
                    pyautogui.write(str(minute_drive))
                    tabing(1)
                
                # Orientation to the hotel
                if ofi != 0:
                    pyautogui.typewrite(str(ofi))
                    tabing(2)
                else:
                    tabing(2)
                
                # Always Tick on Available on GDS and Media
                pyautogui.press('space')
                
                # Click Add
                tabing(1)
                pyautogui.press('enter')
                
                print(f'{code} is Added to DataWeb!!')
            
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

print('Surrounding Attractions Task is Done!')
print('Next Task is Geocoding You have to do it manually!')