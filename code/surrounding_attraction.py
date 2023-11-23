import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *
import pandas as pd

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

# for data enter in add attraction page
def enter_from_df(df, catagory, check_exist=list, unit_select=int):
    # Collect Error
    error = []
    for index, row in df.iterrows():
        if row['name'] not in check_exist:
            code = catagory
            if str(row['orientation']) != 'nan':
                ofi = extract_capital_letters(row['orientation'])
            else:
                ofi = 0
            shuttle = row['shuttle']
            shuttle_service_type = row['shuttle_service']
            distance = row['distance']
            minute_walk = row['time_walk']
            minute_drive = row['time_drive']
            
            # Add
            code_name = surrouding_dict.get(code)
            driver.execute_script(f"addBasicElement('{code}','{code_name}');")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="formTitle"]'))
                )

            # Name
            input_text(element_id='hotelIp.name', text=row['name'])
                            
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
            if str(distance) != 'nan':
                driver.execute_script(f'var DistanceInput = document.getElementById("{unit_select}"); DistanceInput.value = "{distance}"; (document.createEventObject ? DistanceInput.fireEvent("onchange", document.createEventObject()) : DistanceInput.dispatchEvent(new Event("change")));')
       
            # Minute Walk
            if str(minute_walk) == 'nan':
                input_text(element_id='hotelIp.walkingTime', text='99')
            else:
                input_text(element_id='hotelIp.walkingTime', text=str(minute_walk))
                            
            # Minite Drive
            if str(minute_drive) == 'nan':
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
            
    # Print error to user            
    if len(error) != 0:
        for i in error:
            print(f'[ERROR] - {i}')

def add(hotel_rid):
    # set web target
    url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    # get all list in Main Attraction to re check already input item
    cell_list = []
    for i in range(11, 29):
        cell_list.append(f'C{i}')
        
    main_attractions = get_excel_values(file_path=excel_file_path,
                                        sheet_name='Main Attractions',
                                        cell_addresses=cell_list)
    # Get data
    unit_select = get_excel_values(excel_file_path, sheet_name='Main Attractions', cell_addresses=['E8'])

    # Read the Excel file, skipping the first 12 rows, and using the 13th row as column headers
    df = pd.read_excel(excel_file_path, 
                    sheet_name='Other Attractions', 
                    header=12, 
                    )
    df.drop(df.columns[0:2], axis=1, inplace=True)
    df.drop(df.columns[7], axis=1, inplace=True)

    # Rename column
    columns_name = ['name', 'shuttle', 'shuttle_service', 'orientation', 'distance', 'time_walk', 'time_drive']
    df.columns = columns_name

    # df for COMP
    df_comp = df.iloc[0:9]
    df_comp = df_comp[df_comp.iloc[:, 0].notna()]

    # df for CONG
    df_cong = df.iloc[10:18]
    df_cong = df_cong[df_cong.iloc[:, 0].notna()]

    # df for EXHI
    df_exhi = df.iloc[19:27]
    df_exhi = df_exhi[df_exhi.iloc[:, 0].notna()]

    # df for EXPO
    df_expo = df.iloc[28:34]
    df_expo = df_expo[df_expo.iloc[:, 0].notna()]

    # unit select
    if unit_select[0] == 'Km':
        unit_select = 'hotelIp.kilometerDistance'
    else:
        unit_select = 'hotelIp.milesDistance'

    # open target url
    driver.get(url)
    time.sleep(1)
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="allIpsTabLink"]'))
        )
    print(f'[INFO] - {page.text}')

    # Enter Data for 4 df
    enter_from_df(df_comp, catagory='COMP', check_exist=main_attractions, unit_select=unit_select)
    enter_from_df(df_cong, catagory='CONG', check_exist=main_attractions, unit_select=unit_select)
    enter_from_df(df_exhi, catagory='EXHI', check_exist=main_attractions, unit_select=unit_select)
    enter_from_df(df_expo, catagory='EXPO', check_exist=main_attractions, unit_select=unit_select)   
