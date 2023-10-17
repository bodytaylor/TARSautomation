import pyautogui
from functions import *

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
        row += 3
    
    return row_count

# format time object to str
def format_time(time):
    return time.strftime("%H:%M") if time is not None else ""

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Load workbook and read the data
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Bar"  
bars = {}
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Count even rows
        row_count = count_rows(sheet, "B", 14)
        print(f"Content book contain: {row_count} item(s)")

        # Loop through the rows and enter data
        cell_start = 14
        for i in range(row_count):
            # Get data from excel file
            
            bar_code = str(sheet[f"D{cell_start}"].value).split()
            bar_code = str(bar_code[0])
            
            # bar name
            bar_name = sheet[f"B{cell_start}"].value
            
            # Opening Hours information
            open = sheet[f"L{cell_start}"].value
            close = sheet[f"M{cell_start}"].value
            
            # format time object with function
            open_formatted = format_time(open)
            close_formatted = format_time(close)

            # for write open time
            open_hour = f'{open_formatted}-{close_formatted}'
            
            # Max seats
            max_seats = sheet[f"N{cell_start}"].value
            if max_seats == None:
                max_seats = 0
            
            # Average Price -> skip
            
            # Service Tickbox
            pet_allow =     sheet[f"O{cell_start}"].value
            room_service =  sheet[f"P{cell_start}"].value
            light_meal =    sheet[f"Q{cell_start}"].value
            music =         sheet[f"R{cell_start}"].value
            happy_hour =    sheet[f"S{cell_start}"].value
            
            # Opening Date -> skip 5 tabs
            
            # Open information
            mon = sheet[f"E{cell_start}"].value
            tue = sheet[f"F{cell_start}"].value
            wed = sheet[f"G{cell_start}"].value
            thu =  sheet[f"H{cell_start}"].value
            fri =  sheet[f"I{cell_start}"].value
            sat =  sheet[f"J{cell_start}"].value
            sun =  sheet[f"K{cell_start}"].value
            
            # rank = i
            rank = i + 1
            
            # add to dict
            bars[bar_name] = [{'Code': bar_code},
                                     {'Name': bar_name},
                                     {'Opening hours': open_hour},
                                     {'Max seats': max_seats},
                                     {'Services': [
                                        pet_allow,
                                        room_service,
                                        light_meal,
                                        music,
                                        happy_hour   
                                     ]},
                                     {'Open Information': [
                                         mon,
                                         tue,
                                         wed,
                                         thu,
                                         fri,
                                         sat,
                                         sun
                                     ]},
                                     {'Rank': rank}   
            ]
            
            cell_start += 3

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close() 

# Open web browser
url = 'https://dataweb.accor.net/dotw-trans/barTabs!input.action'
open_web(url)
find_logo()
tabing(2)
pyautogui.press('enter')

# Start Looping!
for keys in bars:
    # Locate menu
    find_and_click('img\\type_code.PNG')
    find_searchbox()
    pyautogui.write(bars['Bar'][0]['Code'])
    pyautogui.press('enter')
    
    # Find add button and start entering data
    find_add()
    time.sleep(1)
    find_and_click_on(r'img\add_bar.PNG')
    tabing(3)
    
    # Name
    name = str(bars[f'{keys}'][1]['Name'])
    pyautogui.write(name)
    tabing(1)

    # Oppening Hours
    pyautogui.write(str(bars[f'{keys}'][2]['Opening hours']))
    tabing(1)
    
    # Max seats
    pyautogui.write(str(bars[f'{keys}'][3]['Max seats']))
    tabing(2)
    
    # Service Tickbox
    tickbox(data=bars[f'{keys}'][4]['Services'])
    tabing(4)
    
    # Open Information
    tickbox(data=bars[f'{keys}'][5]['Open Information'])
    tickbox(data=bars[f'{keys}'][5]['Open Information'])
    
    # Rank
    pyautogui.write(str(bars[f'{keys}'][6]['Rank']))
    
    # Find Update Button
    tabing(1)
    pyautogui.press('enter')
    print(f'Bar {keys} has been added!')
    
    # Wait page to load and locate menu again
    find_logo()
    tabing(2)
    pyautogui.press('enter')
    time.sleep(1)
    
    
print(f'All Bar(s) has been loaded to {hotel_rid}!')
print("don't forget to add description!")
