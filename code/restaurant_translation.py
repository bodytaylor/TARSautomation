import time
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Function to count even rows until an empty cell is encountered
def count_rows(sheet, column_letter, start_row):
    row_count = 0
    row = start_row
    
    while True:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            break
        if cell_value is not None:
            row_count += 1
        row += 4
    
    return row_count

# Load workbook and read the data
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Restaurant"  
restaurants = {}
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Count even rows
        row_count = count_rows(sheet, "B", 15)
        print(f"Content book contain: {row_count} item(s)")

        # Loop through the rows and enter data
        cell_start = 15
        for i in range(row_count):
            # Get data from excel file
            rt_name = sheet[f"B{cell_start}"].value
            description = sheet[f"D{cell_start + 2}"].value
            restaurants[rt_name] = description
            cell_start += 4

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()
       
# Check Text 
df = pd.DataFrame(list(restaurants.items()), columns=['rt_name', 'description'])
check_text(df=df, col='description')
check_descrip_len(df=df, col='description')

# Start looping!
for i in range(len(df)):
    rt_name = df.iloc[i, 0]
    search_key = str(rt_name).replace(' ', '+')
    
    # Open webbrowser
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelRestaurant!input.action?actionType=translate&hotelRestaurant.type.code=RT&hotelRestaurant.name={search_key}&hotelRestaurant.codeRest=R00{i + 1}&'
    open_web(url)
    find_logo()
    
    # Click on translation button
    find_and_click_on('img\\translate.png')
    time.sleep(2)
    
    # Click on menu and locate Translate a restaurant input box
    find_and_click_on('img\\translate_rt.PNG')
    time.sleep(1)
    tabing(6)

    # Get data from DataFrame and type in the discription box, do not change the secound locater!
    description = df.iloc[i, 1]
    type_translate(1, description)
    
    # Go to translate button            
    time.sleep(1)
    
    # Hit enter
    pyautogui.press('enter')
    time.sleep(1)

    # Confirm box
    pyautogui.press('enter')
    time.sleep(1)
    
    # Close Browser
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')
    
    # Print result
    print(f'translation for {rt_name} has been added')
    
print(f'Description and translation for restaurants of {hotel_rid} is done!')
