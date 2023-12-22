import pyautogui as pa
import pandas as pd
from functions import *
import ast

## Further update add function for checking data quality before enter to prevent error 
## Meal plan mapping to Worldspan meal plan code
"""
AP-AMERICAN PLAN                                                
BB-BED AND BREAKFAST                                            
BP-BERMUDA PLAN                                                 
CB-CARIBBEAN PLAN                                               
CP-CONTINENTAL PLAN                                             
DB-DINNER BED AND BREAKFAST                                     
EP-EUROPEAN PLAN                                                
FB-FULL BREAKFAST                                               
FP-FAMILY PLAN                                                  
MA-MODIFIED AMERICAN PLAN                                       
RO-ROOM ONLY
"""


def find_gds_windows():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\worldspan.PNG", confidence=0.75)
    print('Please Open GDS - Term Worldspan Prod')
    while image == None:
        image = pyautogui.locateOnScreen(r"img\worldspan.PNG", confidence=0.75)
        time.sleep(1)

hotel_rid = input('Please Enter Hotel RID: ')
file_path = f"gds\worldspan\{hotel_rid} Worldspan.csv"
df = pd.read_csv(file_path, dtype=str)

# Print Code to User
print(f"Use this to check availability: {df['Check availability'].iloc[0]}")
print(f"World Span Code: {df['worldspan code'].iloc[0]}")
print(f"Adding new Property code: HHPA{df['worldspan code'].iloc[0]}")

# Drop Unused Cols
col_to_drop = ['worldspan code', 'Check availability']
df = df.drop(col_to_drop, axis=1)

# Entering add Hotel Page
find_gds_windows()
tabing(5)
prop_code = ['EY', 'LH', 'MD', 'UP']
for index, row in df.iterrows():
    values = row.values
    for value in values:
        str_value = str(value)
        if '[' in str_value:
            a_list = ast.literal_eval(str_value)
            count_tab = 8 - len(a_list)
            for i in a_list:
                pa.typewrite(i)
                tabing(1)
            tabing(count_tab)
        elif str_value in prop_code:
            pa.typewrite(str_value)
            tabing(3)
        elif str_value == 'K':
            pa.typewrite('N/A')
            tabing(1)
        elif str_value == 'nan':
            tabing(1)
        else:
            pa.typewrite(str_value)
            tabing(1)



