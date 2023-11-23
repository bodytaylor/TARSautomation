import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from functions import *
from web_driver_init import driver
from dictionary import *

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

# find type of product
def find_type(df, code):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        return result[2]
    else:
        return None

def add(hotel_rid):
    
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Bar"  
    bars = {}
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            # Count even rows
            result = count_rows(sheet, "D", 14)
            row_count, cell_record = result
            print(f"Content book contain: {row_count} item(s)")

            # Loop through the rows and enter data
            cell_start = 14
            for i, cell in enumerate(cell_record):
                # Get data from excel file
                bar_code = str(sheet[f"D{cell}"].value).split()
                bar_code = str(bar_code[0])
                # bar name
                bar_name = sheet[f"B{cell}"].value
                description = sheet[f"E{cell + 1}"].value
                if description == None:
                    description = sheet[f"E{cell + 2}"].value
                
                # create dict
                bars[bar_name] = [
                    {'Code': bar_code},
                    {'Description': description}
                ] 

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close() 
            
    # collect error message        
    error = []
    
    # Start Looping!
    for keys in bars:
        # find type
        bar_code = bars[f'{keys}'][0]['Code']
        code_type = bar_dic[bar_code]
        description = bars[f'{keys}'][1]['Description']
        key = keys.upper()
        key = url_parse(key)
        # Open webbrowser
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelBar!input.action?actionType=translate&hotelBar.barType.code={bar_code}&hotelBar.name={key}&'
        driver.get(url)
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="barsDescriptionsTable"]'))
            )
        
        # Click on Translate 
        driver.execute_script(f"displayTranslateForm('translateInput','GB','{bar_code}','barsDescriptionsTable','true','true','GB','true');")
        
        # wait for form to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="translateHotelBarFormJson"]'))
            )
        
        # find description box
        description_box = driver.find_element(By.ID, "hotelBarTranslate.description")
        description_box.send_keys(description)
        
        script = """
        document.getElementById('translateHotelBarForm.submitButton').click();
        """
        
        driver.execute_script(script)
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
            
        # get response
        get_response(driver=driver, code=bar_code , error=error)
         
    print(f'All Bar(s) has been loaded to {hotel_rid}!')
    print("don't forget to add description!")
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')
