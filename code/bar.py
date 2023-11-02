import pyautogui
from functions import *

# Function to count even rows until an empty cell is encountered
def count_rows(sheet, column_letter, start_row):
    row_count = 0
    row = start_row
    search = 0
    cell_record = []
    while search <= 5:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            search += 1
        if cell_value is not None:
            row_count += 1
            search = 0
            cell_record.append(row)
        row += 1
    return row_count, cell_record

# format time object to str
def format_time(time):
    return time.strftime("%H:%M") if time is not None else ""

def add(hotel_rid):
    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Bar"  
    bars = {}
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            # Count item(s) in the content book
            result = count_rows(sheet, "D", 14)
            row_count, cell_record = result
            print(f"Content book contain: {row_count} item(s)")
            
            # Loop through the rows and enter data
            for i, cell in enumerate(cell_record):
                # Get data from excel file
                
                bar_code = str(sheet[f"D{cell}"].value).split()
                bar_code = str(bar_code[0])
                
                # bar name
                bar_name = sheet[f"B{cell}"].value
                
                # Opening Hours information
                open = sheet[f"L{cell}"].value
                close = sheet[f"M{cell}"].value
                
                # format time object with function
                open_formatted = format_time(open)
                close_formatted = format_time(close)

                # for write open time
                open_hour = f'{open_formatted}-{close_formatted}'
                
                # Max seats
                max_seats = sheet[f"N{cell}"].value
                if max_seats == None:
                    max_seats = 0
                
                # Average Price -> skip
                
                # Service Tickbox
                pet_allow =     sheet[f"O{cell}"].value
                room_service =  sheet[f"P{cell}"].value
                light_meal =    sheet[f"Q{cell}"].value
                music =         sheet[f"R{cell}"].value
                happy_hour =    sheet[f"S{cell}"].value
                
                # Opening Date -> skip 5 tabs
                
                # Open information
                mon = sheet[f"E{cell}"].value
                tue = sheet[f"F{cell}"].value
                wed = sheet[f"G{cell}"].value
                thu =  sheet[f"H{cell}"].value
                fri =  sheet[f"I{cell}"].value
                sat =  sheet[f"J{cell}"].value
                sun =  sheet[f"K{cell}"].value
                
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
    find_and_click('img\\type_code.PNG')
    
    # Start Looping!
    for keys in bars:
        code_search(bars[f'{keys}'][0]['Code'])
        
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
