import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  web_driver_init import driver
import openpyxl
import pandas as pd
from functions import *

# search for non accepted charecters in data frame
def check_text_meet(df, col,):
    df['Non_Matching_Chars'] = df[col].apply(find_non_matching_chars)
    accept = 0
    for index, row in df.iterrows():
        non_matching_chars = row['Non_Matching_Chars']
        if non_matching_chars:
            print(f"Row {df.iloc[index, 0]} column {col}: Detected characters: '{non_matching_chars}'")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()
    return accept

# Check Description lengh
def check_descrip_len(df, col):
    accept = 0
    for index, description in df.iterrows():
        if len(description) > 255:
            print(f"Row {df.iloc[index, 0]} column {col}: contain more than 255 charactors")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()
    return accept

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
    

# function for input description into translation page
def enter_description(keys, search_key, description):
    # Open new tab and locate menu
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelLoungeInput.action?actionType=translate&description.lounge.type.code=MEET&description.lounge.name={search_key}'
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "zoneCliquable"))
        )
    
    # Click on the element
    driver.execute_script("displayTranslateForm('GB','MEET','true','true','GB','true');")
    time.sleep(1)
        
    # Enter Translations
    textarea = driver.find_element(By.ID, "hotelLoungeTranslation.description.text")
    textarea.send_keys(description[f'{keys}'])
    time.sleep(1)
    
    # Click on Translate button
    script = """
    document.getElementById('translateHotelLoungeForm.submitButton').click();
    """
    driver.execute_script(script)
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()

def add(hotel_rid):
    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Meeting Room"  
    description = {}
    error = []
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            # Count even rows
            even_row_count = count_even_rows(sheet, "C", 12)
            print("Count of even rows until an empty cell:", even_row_count)

            # Loop through the rows and enter data
            cell_start = 12
            for i in range(even_row_count):
                description[sheet[f"C{cell_start}"].value] = (sheet[f"E{cell_start + 1}"].value)
                cell_start += 2

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Close the workbook
        if workbook:
            workbook.close()
            
        # Create df
        while True:
            df = pd.DataFrame(list(description.items()), columns=['meet_room', 'description'])

            # Check Discription before entering it
            text = check_text_meet(df=df, col='description')
            text_len = check_descrip_len(df=df, col='description')
            if text == text_len == 0:
                break
            continue_program()

        # If all pass, Add translation
        for key in description:
            search_key = url_parse(str(key).strip())
            enter_description(keys=key, search_key=search_key, description=description)
            get_response(driver=driver, code=search_key, error=error)
            
        print(f'Translation Added to all meeting rooms in {hotel_rid}')
        if len(error) != 0:
            for i in error:
                print(f'[ERROR] - {i}')
