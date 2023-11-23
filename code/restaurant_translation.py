import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from functions import *
from web_driver_init import driver

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

def add(hotel_rid):
    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Restaurant"  
    restaurants = {}
    error = []
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
    while True:
        sp_char = check_text(df=df, col='description')
        des_len = check_descrip_len(df=df, col='description')
        if sp_char == des_len == 0:
            break
        continue_program()
        
    # Start looping!
    for i in range(len(df)):
        rt_name = df.iloc[i, 0]
        search_key = str(rt_name).replace(' ', '+')
        
        # Open webbrowser
        url = f'https://dataweb.accor.net/dotw-trans/translateHotelRestaurant!input.action?actionType=translate&hotelRestaurant.type.code=RT&hotelRestaurant.name={search_key}&hotelRestaurant.codeRest=R00{i + 1}&'
        driver.get(url)
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="restaurantsDescriptionsTable"]'))
            )

        # Click on Translate 
        driver.execute_script(f"displayTranslateForm('translateInput','GB','RT','restaurantsDescriptionsTable','true','true','GB','true');")
        
        # wait for form to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="translateHotelRestaurantFormJson"]'))
            )
        
        # find description box
        description_box = driver.find_element(By.ID, "hotelRestaurantTranslate.description")
        
        # Get data from DataFrame and type in the discription box, do not change the secound locater!
        description = df.iloc[i, 1]
        description_box.send_keys(description)
        
        script = """
        document.getElementById('translateHotelRestaurantForm.submitButton').click();
        """
        
        driver.execute_script(script)
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
            
        # get response
        get_response(driver=driver, code='RT', error=error)
        
    print(f'Description and translation for restaurants of {hotel_rid} is done!')
