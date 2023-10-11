import time
import pyautogui
import re
import pandas as pd
from functions import *

# for data enter in add attraction page
def enter_from_df(df, catagory):
    for index, row in df.iterrows():
        code = catagory
        if str(row['orientation']) != 'nan':
            ofi = extract_capital_letters(row['orientation'])
        else:
            ofi = 0
        shuttle = row['shuttle']
        shuttle_service_type = row['shuttle_service']
        distance = row['distance']
        minute_walk = row['time_walk']
        minute_drive = row['time_drive']
                    
        if code in choice_list:
            choice = 2
        else:
            choice = 1

        search_with_choice(code, choice=choice)
        find_add()
        time.sleep(1)
        find_and_click_on(r'img\add_surrounding.PNG')
        tabing(2)

        # Name
        pyautogui.write(row['name'])
                        
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
        if str(distance) != 'nan':
            pyautogui.write(str(distance))
            tabing(1)
        else:
            tabing(1)
                        
        # Minute Walk
        if str(minute_walk) == 'nan':
            pyautogui.write('99')
        else:
            pyautogui.write(str(minute_walk))
            print(minute_walk)
        tabing(1)
                        
        # Minite Drive
        if str(minute_drive) == 'nan':
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
                        
        print(f'{code} is Added to Data Web!!')

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# set web target
url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Main Attractions"
load_excel_file(excel_file_path, sheet_name)

choice_list = [
    'ADMI', 'ENT', 'APAR', 'AQU', 'ARTC', 'PLGA', 'BOT', 'EVNT', 'CAS', 'CINE', 
    'CLIN', 'COLL', 'COMP', 'CONC', 'CONG', 'CULT', 'EMBA', 'ENTE', 'ENTC', 'EVNS',
    'EXHI', 'EXPO', 'GOLF', 'HIST', 'HOPI', 'INDU', 'LAKE', 'MALL', 'MILI', 'MOVI',
    'MUSM', 'TSP', 'OPE', 'OATT', 'OTBU', 'RELI', 'CTR1', 'RAC', 'REST', 'SCHO',
    'SHOM', 'PIST', 'DIVE', 'TOUR', 'CSPO', 'SPOR', 'STAD', 'ATOU', 'INFO', 'WORL',
    'ZOO', 'PZOO'
]
# Get data
unit_select = get_excel_values(excel_file_path, sheet_name=sheet_name, cell_addresses=['E8'])

sheet_name = 'attraction'

# Read the Excel file, skipping the first 12 rows, and using the 13th row as column headers
df = pd.read_excel(excel_file_path, 
                   sheet_name='Other Attractions', 
                   header=12, 
                   )
df.drop(df.columns[0:2], axis=1, inplace=True)
df.drop(df.columns[7], axis=1, inplace=True)

# Rename column
columns_name = ['name', 'shuttle', 'shuttle_service', 'orientation', 'distance', 'time_walk', 'time_drive']
df.columns = columns_name

# df for COMP
df_comp = df.iloc[0:9]
df_comp = df_comp[df_comp.iloc[:, 0].notna()]

# df for CONG
df_cong = df.iloc[10:18]
df_cong = df_cong[df_cong.iloc[:, 0].notna()]

# df for EXHI
df_exhi = df.iloc[19:27]
df_exhi = df_exhi[df_exhi.iloc[:, 0].notna()]

# df for EXPO
df_expo = df.iloc[28:34]
df_expo = df_expo[df_expo.iloc[:, 0].notna()]

# unit select
if unit_select[0] == 'Km':
    unit_select = 2
else:
    unit_select = 1

# open target url
open_web(url)

# Enter Data for 4 df
enter_from_df(df_comp, catagory='COMP')
enter_from_df(df_cong, catagory='CONG')
enter_from_df(df_exhi, catagory='EXHI')
enter_from_df(df_expo, catagory='EXPO')
