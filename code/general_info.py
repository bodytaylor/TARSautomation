from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import *
from dictionary import *

# Check Date time object
def check_and_convert_to_datetime(input_value):
    if input_value is None:
        return None
    
    if isinstance(input_value, datetime):
        return input_value
    
    try:
        return datetime.strptime(input_value, "%d/%m/%Y")
    except ValueError:
        return None
    
# Extract currency from text
def extract_currentcy(input):
    pattern = r'-(.+)'
    match = re.search(pattern, input)
    if match:
        result = match.group(1).strip()
    else:
        result = None   
    return result

# input function in console
# input textbox
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.15)
    
# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.15)

def click_button(element):
    driver.execute_script(f'document.getElementById("{element}").click();')
    time.sleep(0.15)

def add(hotel_rid):  
# Ask user for Check paris time and input
    dif_time = str(input("Please visit: https://www.zeitverschiebung.net/en/country/fr \nAnd input different time here: "))

    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['C57', 'J57', 'D12', 'K10', 'J6', 'J63', 'C61', 'J59', 'C59', 'K65', 'C63', 'C65'], 
        sheet_name='Address&Setup'
    )

    # always tick on Message to the hotel on AH.com
    ## All text input ##
    # Construction date : C57 
    con_date = data[0]
    con_date = check_and_convert_to_datetime(con_date)
    if type(con_date) == datetime:
        con_date = con_date.strftime("%d/%m/%Y")

    # Last renovation date : J57 
    last_reno = data[1]
    last_reno = check_and_convert_to_datetime(last_reno)
    if type(last_reno) == datetime:
        last_reno = last_reno.strftime("%d/%m/%Y")
  
    # Distribution date : D12 
    tar_dis_date = data[2]
    tar_dis_date = check_and_convert_to_datetime(tar_dis_date)
    if type(tar_dis_date) == datetime:
        tar_dis_date = tar_dis_date.strftime("%d/%m/%Y")

    # Opening date : K10 
    open_date = data[3]
    open_date = check_and_convert_to_datetime(open_date)
    if type(open_date) == datetime:
        open_date = open_date.strftime("%d/%m/%Y")

    # Limit time for reservation : always 23:59 -> text
    limit_time = "23:59"

    # Nb of hours / Paris :
    nb_hour_paris = dif_time

    # Longitude : skip
    # Latitude :  skip
    # Domain :    skip
    # Language of the faxes received : Defult Language

    # Number of lifts : K65  
    nb_lifts = data[9]

    # Number of rooms : C63  
    nb_rooms = data[10]

    # Number of floors : C65
    nb_floors = data[11]

    # create text dict
    text_dict = {
        "gi_constructionDate": con_date,
        "gi_lastRenovDate": last_reno,
        "gi_tarsCreatDate": tar_dis_date,
        "gi_openingDate": open_date,
        "gi.limitHour": limit_time,
        "gi.nbOfHours": nb_hour_paris,
        "gi.nbOfLifts": nb_lifts,
        "gi.nbOfRooms": nb_rooms,
        "gi.nbOfFloors": nb_floors
    }

    ## All Dropdown menu ##
    # Lodging type : J63
    lodging_type = data[5]
    lodging_value = search_key(dict=lodging_type_dict, search_value=lodging_type)

    # Standard of hotel : in R_referrence for hotel creation
    brand = data[4]
    standard = standard_dict[brand]

    # Environment : C61   
    environment = data[6]
    environment_value = enviro_dict[environment]

    # Location : J59
    location = data[7]
    location_value = location_dict[location]

    # Operation area : None
    # TARS currency : C59
    currency = data[8]
    currency_value = extract_currentcy(currency)

    # PMS currency : C59
    pms_currency_value = currency_value

    # Conversion currency :  None
    # Create dropdown dict
    dropdown_dict = {
        "selectLodging": lodging_value,
        "selectStandard": standard,
        "selectEnvironment": environment_value,
        "selectLocation": location_value,
        "selectCurrency": currency_value,
        "selectPmsCurrency": pms_currency_value
    }

    # walk to this url
    driver.get("https://dataweb.accor.net/dotw-trans/displayGeneralInformation!input.action")
    page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="generalInformationLink"]'))
        )
    print(f'[INFO] - {page.text}')

    # input data in console
    ## input text data ##
    for key, value in text_dict.items():
        input_text(element_id=key, text=value)

    ## input dropdown data ##
    for key, value in dropdown_dict.items():
        select_dropdown(element_id=key, value=value)

    ## Tick on message to all accor.com
    driver.execute_script('document.getElementById("gi.mesToHotelOnAH").checked = true;')

    print('Automation Done Please Review The input data before click save! Thanks.')