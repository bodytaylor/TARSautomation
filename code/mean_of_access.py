import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
import re
from functions import *

# execute java script
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)
        
def enter_data(data):
    element_list = [
        'hotelAccess.name', 'hotelAccess.direction', 'hotelAccess.line', 'hotelAccess.station'
    ]
    # Loop through the data and enter it
    for i, value in enumerate(data):
        if value != None:
            input_text(element_id=element_list[i], text=value)
            time.sleep(0.1)
        
# menu dict
mean_of_acces_dict = {
    'RER': 'By RER',
    'BUSS': 'By bus',
    'AUT1': 'By car',
    'AUT2': 'By car',
    'AUTO': 'By car',
    'CARE': 'By car from the east',
    'CARN': 'By car from the north',
    'CARS': 'By car from the south',
    'CARW': 'By car from the west',
    'FERR': 'By ferry',
    'CBUS': 'By free shuttle/courtesy bus',
    'PORT': 'By harbour',
    'HELI': 'By helicopter',
    'LIMO': 'By limousine',
    'MOTR': 'By motorway',
    'MOTE': 'By motorway from the east',
    'MOTN': 'By motorway from the north',
    'MOTS': 'By motorway from the south',
    'MOTW': 'By motorway from the west',
    'AERO': 'By plane',
    'AIR1': 'By plane',
    'RAIL': 'By railway',
    'ROUT': 'By road',
    'METR': 'By subway',
    'TAXI': 'By taxi',
    'TRAM': 'By tram',
    'ACCM': 'Means of access',
    'WALK': 'On foot',
    'PBUS': 'Paying Shuttle',
    }

def add(hotel_rid):
    # Read data from Excel file
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Address&Setup"
    code_list = []
    load_excel_file(excel_file_path, sheet_name)

    # error
    error = []
    # Open Webpage
    url = 'https://dataweb.accor.net/dotw-trans/accessTabs!input.action'
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelAccessesTable"]'))
        )
    
    # add
    driver.execute_script("addBasicElement('ACCM','Means of access');")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelAccessFormDiv"]'))
        )

    # Enter Hotel name
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            hotel_name = sheet['C4'].value
            input_text(element_id='hotelAccess.name', text=hotel_name)
            driver.execute_script("submitFormAccess();")
            time.sleep(2) 
            
            # add translation 
            hotel_direction = sheet['C84'].value          
            hotel_name_url = str(hotel_name).replace(" ", "+")
            url_translation = f'https://dataweb.accor.net/dotw-trans/translateHotelAccess!input.action?actionType=translate&hotelAccess.accessType.code=ACCM&hotelAccess.name={hotel_name_url}&'
            driver.get(url_translation)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="accessesDescriptionsTable"]'))
                )
            # Add
            driver.execute_script(f"displayTranslateForm('translateInput','GB','ACCM','accessesDescriptionsTable','true','true','GB','true');")
            time.sleep(1)
            # Input Translation
            input_text(element_id='hotelAccessTranslate.translatedDescription', text=hotel_direction)
            # Click on Translate button
            script = """
            document.getElementById('translateHotelAccessForm.submitButton').click();
            """
            driver.execute_script(script)
            time.sleep(1)
            alert = driver.switch_to.alert
            alert.accept()
            
            # Print the response
            WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="messages"]'))
                ) 
            time.sleep(0.5)
            try:
                action_message_element = WebDriverWait(driver, 7).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]'))
                    )
                action_message = action_message_element.find_element(By.TAG_NAME, 'span').text
                print(f'[INFO] - {action_message}')
            except:
                error_message = action_message_element = WebDriverWait(driver, 7).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="errormessage"]'))
                    )
                error.append(f'{code}: {error_message.text}')
                print(f'[INFO] - {error_message.text}')
            
            # Add another attraction
            # Open Webpage
            url = 'https://dataweb.accor.net/dotw-trans/accessTabs!input.action'
            driver.get(url)
            WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelAccessesTable"]'))
            )
            
            for i in range(4):
                if sheet[f'E{149 + i}'].value != None:
                    pattern = r'([A-Z]+) -'
                    code = re.findall(pattern, sheet[f'C{149 + i}'].value)[0]
                    code_list.append(code)
                    data = [sheet[f'E{149 + i}'].value,
                            sheet[f'H{149 + i}'].value,
                            sheet[f'I{149 + i}'].value,
                            sheet[f'K{149 + i}'].value]
                    
                    acc_name = mean_of_acces_dict.get(code)
                    
                    # Add surrounding
                    driver.execute_script(f"addBasicElement('{code}','{acc_name}');")
                    enter_data(data)
                    
                    # Click add
                    driver.execute_script("submitFormAccess();")
                    
                    # Print the response
                    WebDriverWait(driver, 7).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="messages"]'))
                        ) 
                    time.sleep(0.5)
                    try:
                        action_message_element = WebDriverWait(driver, 7).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="actionmessage"]'))
                            )
                        action_message = action_message_element.find_element(By.TAG_NAME, 'span').text
                        print(f'[INFO] - {action_message}')
                    except:
                        error_message = action_message_element = WebDriverWait(driver, 7).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="errormessage"]'))
                            )
                        error.append(f'{code}: {error_message.text}')
                        print(f'[INFO] - {error_message.text}')
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close()
            
    print(f'Mean of Access has been added to {hotel_rid}!')
    print('Next Step Add Surrounding Attractions')
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')
