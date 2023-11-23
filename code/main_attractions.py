import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
import re
from functions import *

# attractions dict
surrouding_dict = {
    'ADML':	'Administrative Location',
    'AIRP':	'Airport',
    'SKI': 'At a ski lift',
    'BAR': 'Bar',
    'BAY': 'Bay',
    'BUS': 'Bus stop',
    'AFFA':	'Business & financial district',
    'CANL':	'Canal',
    'CITY':	'City center',
    'DOWN':	'City downtown',
    'NCIT':	'Closest major urban centre',
    'CENT':	'Distance from city centre',
    'NPT1':	'Domestic airport 1 - full name',
    'NAP1':	'Domestic airport 1 - IATA code',
    'NPT2':	'Domestic airport 2 - full name',
    'NAP2':	'Domestic airport 2 - IATA code',
    'NPT3':	'Domestic airport 3 - full name',
    'NAP3':	'Domestic airport 3 - IATA code',
    'THEA':	'Entertainment/theatre district',
    'FERR':	'Ferries',
    'HELI':	'Helipad/aerodrome',
    'HEXI':	'Highway exit',
    'APT1':	'Int. airport 1 - full name',
    'AER1':	'Int. airport 1 - IATA code',
    'APT2':	'Int. airport 2 - full name',
    'AER2':	'Int. airport 2 - IATA code',
    'APT3':	'Int. airport 3 - full name',
    'AER3':	'Int. airport 3 - IATA code',
    'APT4':	'Int. airport 4 - full name',
    'AER4':	'Int. airport 4 - IATA code',
    'APT5':	'Int. airport 5 - full name',
    'AER5':	'Int. airport 5 - IATA code',
    'MARI':	'Marina',
    'HARD':	'Marine terminal',
    'METR':	'Metro/underground/subway',
    'MONT':	'Mountain',
    'NAPA':	'National park',
    'PLGN':	'Nearby',
    'NCC': 'Nearest major city - code',
    'NCN': 'Nearest major city - name',
    'PLAG':	'On the beach',
    'VIEW':	'Panoramic view',
    'PARK':	'Park',
    'PCC': 'Primary city code',
    'PCN': 'Primary city name',
    'STAT':	'Railway and underground station',
    'GARE':	'Railway station',
    'RSTO':	'Restaurant',
    'RIVE':	'River',
    'SHOP':	'Shopping district',
    'THTR':	'Theatre',
    'SNCF':	'TRAIN + HOTEL GARE SNCF',
    'TRAM':	'Tramway',
    'VALL':	'Valley',
    'SVIE':	'With sea view',
    'WOOD':	'Wood/forest',
    'ADMI':	'Administrative building',
    'ENT': 'Amusement park',
    'APAR':	'Amusement park',
    'AQU': 'Aquarium',
    'ARTC':	'Art and Culture',
    'PLGA':	'Beach area',
    'BOT': 'Botanical gardens',
    'EVNT':	'Business centre',
    'CAS': 'Casino',
    'CINE':	'Cinema district',
    'CLIN':	'Clinic/hospital',
    'COLL':	'College/university',
    'COMP':	'Company',
    'CONC':	'Concert hall',
    'CONG':	'Convention centre',
    'CULT':	'Cultural centre',
    'EMBA':	'Embassy',
    'ENTE':	'Entertainment and theatre',
    'ENTC':	'Entertainment centre',
    'EVNS':	'Events centre',
    'EXHI':	'Exhibition and convention centre',
    'EXPO':	'Exhibition centre',
    'GOLF':	'Golf course',
    'HIST':	'Historic monument',
    'HOPI':	'Hospital',
    'INDU':	'Industrial area',
    'LAKE':	'Lake',
    'MALL':	'Mall and Shopping Centre',
    'MILI':	'Military base',
    'MOVI':	'Movie theatre',
    'MUSM':	'Museums',
    'TSP': 'Nearest transport',
    'OPE': 'Opera/symphony/concert hall',
    'OATT':	'Other attractions',
    'OTBU':	'Other point of business interest',
    'RELI':	'Place of worship',
    'CTR1':	'Primary point of interest',
    'RAC': 'Racetrack',
    'REST':	'Restaurant and cafe district',
    'SCHO':	'School/university',
    'SHOM':	'Shopping centre/mall',
    'PIST':	'Ski area',
    'DIVE':	'Special tourist area',
    'TOUR':	'Special tourist area',
    'CSPO':	'Sports centre',
    'SPOR':	'Sports centre',
    'STAD':	'Stadium',
    'ATOU':	'Tourist attraction',
    'INFO':	'Tourist information',
    'WORL':	'World Trade Center',
    'ZOO':	'Zoo',
    'PZOO':	'Zoological park',
    }

# execute java script
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')

# Tickbox in browser console
def tick_box(element):
    script = (f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
    driver.execute_script(script)

# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')

# Extract Capital Letter
def extract_capital_letters(input_string):
    # Define the regular expression pattern to match capital letters
    pattern = r'[A-Z]'
    
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)
    
    # Convert the matches to a string
    capital_letters = ''.join(matches)
    
    return capital_letters

def add(hotel_rid):
    
   # Load Data from Excel 
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Main Attractions"
    load_excel_file(excel_file_path, sheet_name)
    
    url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
    driver.get(url)
    time.sleep(1)
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="allIpsTabLink"]'))
        )
    print(f'[INFO] - {page.text}')
    
    # Collect Error
    error = []

    # Loop Start Here!
    try:
        # Load Excel file and select the sheet
        workbook, sheet = load_excel_file(excel_file_path, sheet_name)
        
        if workbook and sheet:
            # Loop over data file
            cell_start = 11
            # Check Unit Select
            if sheet['E8'].value == 'Km':
                unit_select = 'hotelIp.kilometerDistance'
            else:
                unit_select = 'hotelIp.milesDistance'
            
            for i in range(18):
                if sheet[f'C{cell_start + i}'].value != None:
                    # regex for extract text
                    pattern = r'([^:]+):'
                    extract_cap = r'[A-Z]'
                    
                    # data from excel
                    code = re.findall(pattern, sheet[f'B{cell_start + i}'].value)[0]
                    if sheet[f'G{cell_start + i}'].value != None:
                        ofi = extract_capital_letters(sheet[f'G{cell_start + i}'].value)
                    else:
                        ofi = 0
                    shuttle = str(sheet[f'D{cell_start + i}'].value)
                    shuttle_service_type = str(sheet[f'E{cell_start + i}'].value)
                    distance = (sheet[f'I{cell_start + i}'].value)
                    minute_walk = (sheet[f'J{cell_start + i}'].value)
                    minute_drive = (sheet[f'K{cell_start + i}'].value)

                    # Add
                    code_name = surrouding_dict.get(code)
                    driver.execute_script(f"addBasicElement('{code}','{code_name}');")
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                        )
                    
                    # Write Name
                    input_text(element_id='hotelIp.name', text=sheet[f'C{cell_start + i}'].value)
                    
                    # Shuttle service
                    if ((shuttle == 'Yes free') or (shuttle == 'Yes paying')): # Tick on Shuttle
                        driver.execute_script('var checkbox = document.getElementById("hotelIp.shuttle"); checkbox.checked = !checkbox.checked; changeShuttleValue();')
                        if shuttle_service_type == 'On call':
                            tick_box(element='hotelIp.shuttle.onCall')

                        if shuttle_service_type == 'Scheduled':
                            tick_box(element='hotelIp.shuttle.scheduled')
                            
                        if shuttle == 'Yes free':
                            tick_box(element='hotelIp.shuttle.free')

                    # Distance 
                    if distance != None:
                        driver.execute_script(f'var DistanceInput = document.getElementById("{unit_select}"); DistanceInput.value = "{distance}"; (document.createEventObject ? DistanceInput.fireEvent("onchange", document.createEventObject()) : DistanceInput.dispatchEvent(new Event("change")));')
                    
                    # Minute Walk
                    if minute_walk == None:
                        input_text(element_id='hotelIp.walkingTime', text='99')
                    else:
                        input_text(element_id='hotelIp.walkingTime', text=str(minute_walk))
                    
                    # Minite Drive
                    if minute_drive == None:
                        pass
                    else:
                        input_text(element_id='hotelIp.carTime', text=str(minute_drive))
                    
                    # Orientation to the hotel
                    if ofi != 0:
                        select_dropdown(element_id='hotelIp.orientation', value=str(ofi))
                    
                    # Always Tick on Available on GDS and Media
                    tick_box(element='hotelIp.availableOnGdsMedia')
                    
                    # Click Add
                    driver.execute_script('submitFormIp();')
                    
                    # Print the response
                    get_response(driver=driver, code=code, error=error)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the workbook
        if workbook:
            workbook.close()

    print('Surrounding Attractions Task is Done!')
    print('Next Task is Geocoding You have to do it manually!')
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')