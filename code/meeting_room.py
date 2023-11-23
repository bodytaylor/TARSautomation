import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
import openpyxl
from functions import *

# execute java script
def tick_box_script(element, value):
    if value != None:
        driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
        time.sleep(0.1)

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)

# Function to count even rows until an empty cell is encountered
def count_even_rows(sheet, column_letter, start_row):
    even_row_count = 0
    row = start_row
    
    while True:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            break
        if row % 2 == 0:
            even_row_count += 1
        row += 2
    
    return even_row_count

# Function to load Excel file and select the sheet
def load_excel_file(file_path, sheet_name):
    try:
        # Open the Excel file
        workbook = openpyxl.load_workbook(file_path, read_only=True)

        # Select the specific sheet
        sheet = workbook[sheet_name]

        return workbook, sheet

    except Exception as e:
        print(f"An error occurred while loading the Excel file: {str(e)}")
        return None, None

# Function to enter data into a web page
def enter_data(data):
    elements_list = ['hotelLounge.name', 'hotelLounge.surface', 'hotelLounge.maxNumberPax', 
                     'hotelLounge.ceilingHeight', 'hotelLounge.floorCover', 'hotelLounge.nbPaxBoardRoom',
                     'hotelLounge.nbPaxInU', 'hotelLounge.nbPaxClassRoom',
                     'hotelLounge.nbPaxInV', 'hotelLounge.nbPaxTheater', 'hotelLounge.nbPaxRoundTables',
                     'hotelLounge.nbPaxRoundTablesOff', 'hotelLounge.nbPaxRoundTablesDc',
                     'hotelLounge.nbPaxRoundTablesOffDc']
    
    # Loop through the data and enter it
    for i, value in enumerate(data):
        if value == None:
            input_text(element_id=elements_list[i], text='0')
        else:
            input_text(element_id=elements_list[i], text=str(value))

# Handle tickboxes
def tick_box (tickbox):
    tick_box_elements = [
        'hotelLounge.buffet', 'hotelLounge.buffetDc', 
        'hotelLounge.cocktail', 'hotelLounge.exposition'
        ]
    for i, value in enumerate(tickbox):
        if value == 'Yes':
            tick_box_script(element=tick_box_elements[i], value=value)

def add(hotel_rid):
    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Meeting Room"  
    description = {}
    # Open web browser and navigate to a page
    driver.get('https://dataweb.accor.net/dotw-trans/displayHotelLounges!input.action')
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelLoungesTable"]'))
        )
    
    # Error
    error = [] 
               
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            # Count even rows
            even_row_count = count_even_rows(sheet, "C", 12)
            print("Meeting room count:", even_row_count)

            # Loop through the rows and enter data
            cell_start = 12
            for i in range(even_row_count):
                data = [
                        str(sheet[f"C{cell_start}"].value).strip(),
                        int(round((sheet[f"G{cell_start}"].value), 0)),
                        sheet[f"F{cell_start}"].value,
                        round((sheet[f"H{cell_start}"].value), 2),
                        sheet[f"I{cell_start}"].value,
                        sheet[f"L{cell_start}"].value,
                        sheet[f"N{cell_start}"].value,
                        sheet[f"J{cell_start}"].value,
                        sheet[f"M{cell_start}"].value,
                        sheet[f"K{cell_start}"].value,
                        sheet[f"O{cell_start}"].value,
                        sheet[f"Q{cell_start}"].value,
                        sheet[f"P{cell_start}"].value,
                        sheet[f"R{cell_start}"].value
                        ]
                tickbox = [sheet[f"S{cell_start}"].value,
                        sheet[f"T{cell_start}"].value,
                        sheet[f"U{cell_start}"].value,
                        sheet[f"V{cell_start}"].value]
                description[sheet[f"C{cell_start}"].value] = (sheet[f"E{cell_start + 1}"].value)
                
                # Add MEET
                driver.execute_script("addBasicElement('MEET');")
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                    )
                time.sleep(1)
                
                # Enter data into the web page
                enter_data(data)
                tick_box(tickbox)
                
                # Click Add
                driver.execute_script("if(validateForm_hotelLoungeForm($('hotelLoungeForm'))){submitLoungeForm ($('hotelLoungeForm'));}")
                
                # Print the response
                get_response(driver=driver, code=data[0] , error=error)
                    
                cell_start += 2

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close()

    # instruction for next step
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')
    print('Add meeting room successfully!!')
    print('Next add translation. . .')
