import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import load_excel_file
from functions import *

# bar dict
bar_dict = {
    'BAR1':	'AMERICAN BAR',
    'BAR': 'BAR',
    'IBI99': 'bar',
    'IBI01': 'bar-rendez-vous',
    'BAR7':	'DISCOTHEQUE BAR',
    'BAR6': 'LOBBY BAR',
    'LOUNGE': 'LOUNGE',
    'BAR4':	'PIANO BAR',
    'BAR2':	'POOL BAR',
    'BAR3': 'POOL SIDE SNACK BAR',
    'PRIVBA': 'PRIVATE BAR',
    'PUB': 'PUB',
    'SNACBA': 'SNACK-BAR',
    'WINBAR': 'WINE BAR',
    }

# java script execute
def tick_box(element, value):
    if value != None:
        driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
        time.sleep(0.1)

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)

def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.1)

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
            
    # collect error data
    error = []        

    # Open web browser
    url = 'https://dataweb.accor.net/dotw-trans/barTabs!input.action'
    driver.get(url)
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="barTypesTable"]'))
        )
    
    # Start Looping!
    for keys in bars:
        bar_code = bars[f'{keys}'][0]['Code']
        bar_code_name = bar_dict.get(bar_code)
        driver.execute_script(f"addBasicElement('{bar_code}','{bar_code_name}');")
        
        # Name
        name = str(bars[f'{keys}'][1]['Name'])
        input_text(element_id='hotelBar.name', text=name)

        # Opening Hours
        opening_hour = str(bars[f'{keys}'][2]['Opening hours'])
        input_text(element_id='hotelBar.openingHours', text=opening_hour)
        
        # Max seats
        max_guest = (str(bars[f'{keys}'][3]['Max seats']))
        input_text(element_id='hotelBar.maxSeats', text=max_guest)
        
        # Service Tickbox
        service_data = bars[f'{keys}'][4]['Services']
        tick_box(element='hotelBar.petsAllowed', value=service_data[0])
        tick_box(element='hotelBar.roomService', value=service_data[1])
        tick_box(element='hotelBar.lightMeal', value=service_data[2])
        tick_box(element='hotelBar.musicalAnimation', value=service_data[3])
        tick_box(element='hotelBar.happyHour', value=service_data[4])
        
        # Open Information
        midday_data = bars[f'{keys}'][5]['Open Information']
        tick_box(element='hotelBar.mondayMidday', value=midday_data[0])
        tick_box(element='hotelBar.tuesdayMidday', value=midday_data[1])
        tick_box(element='hotelBar.wednesdayMidday', value=midday_data[2])
        tick_box(element='hotelBar.thursdayMidday', value=midday_data[3])
        tick_box(element='hotelBar.fridayMidday', value=midday_data[4])
        tick_box(element='hotelBar.saturdayMidday', value=midday_data[5])
        tick_box(element='hotelBar.sundayMidday', value=midday_data[6])
        
        even_data = bars[f'{keys}'][5]['Open Information']
        tick_box(element='hotelBar.mondayEvening', value=even_data[0])
        tick_box(element='hotelBar.tuesdayEvening', value=even_data[1])
        tick_box(element='hotelBar.wednesdayEvening', value=even_data[2])
        tick_box(element='hotelBar.thursdayEvening', value=even_data[3])
        tick_box(element='hotelBar.fridayEvening', value=even_data[4])
        tick_box(element='hotelBar.saturdayEvening', value=even_data[5])
        tick_box(element='hotelBar.sundayEvening', value=even_data[6])
        
        # Rank
        bar_rank = str(bars[f'{keys}'][6]['Rank'])
        input_text(element_id='hotelBar.rank', text=bar_rank)
        
        # Find Update Button
        driver.execute_script('submitFormBar();')
        time.sleep(1)
        
        # get response
        get_response(driver=driver, code=bar_code , error=error)

    # print result to user     
    print(f'All Bar(s) has been loaded to {hotel_rid}!')
    print("don't forget to add description!")
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')
