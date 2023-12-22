from datetime import datetime
from TarsAutomation import driver, logger
import TarsAutomation as ta
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

def add(hotel_rid, hotel_content):  
    # Ask user for Check paris time and input
    dif_time = str(input("Please visit: https://www.zeitverschiebung.net/en/country/fr \nAnd input different time here: "))

    # always tick on Message to the hotel on AH.com
    ## All text input ##
    # Construction date : C57 
    con_date = hotel_content.construction_date
    con_date = check_and_convert_to_datetime(con_date)
    if type(con_date) == datetime:
        con_date = con_date.strftime("%d/%m/%Y")

    # Last renovation date : J57 
    last_reno = hotel_content.reno_date
    last_reno = check_and_convert_to_datetime(last_reno)
    if type(last_reno) == datetime:
        last_reno = last_reno.strftime("%d/%m/%Y")
  
    # Distribution date : D12 
    tar_dis_date = hotel_content.distribute_tars_date
    tar_dis_date = check_and_convert_to_datetime(tar_dis_date)
    if type(tar_dis_date) == datetime:
        tar_dis_date = tar_dis_date.strftime("%d/%m/%Y")

    # Opening date : K10 
    open_date = hotel_content.open_date
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
    nb_lifts = hotel_content.nb_lifts

    # Number of rooms : C63  
    nb_rooms = hotel_content.nb_rooms

    # Number of floors : C65
    nb_floors = hotel_content.nb_floors

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
    lodging_type = hotel_content.lodging_type
    lodging_value = lodging_type_dict.get(lodging_type)

    # Standard of hotel : in R_referrence for hotel creation
    brand = hotel_content.brand
    standard = standard_dict[brand]

    # Environment : C61   
    environment = hotel_content.environment
    environment_value = enviro_dict[environment]

    # Location : J59
    location = hotel_content.location
    location_value = location_dict[location]

    # Operation area : None
    # TARS currency : C59
    currency_value = hotel_content.currency_code

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

    # Let Rolls!
    ta.get("https://dataweb.accor.net/dotw-trans/displayGeneralInformation!input.action")

    ## input text data ##
    for key, value in text_dict.items():
        ta.input_text(element_id=key, text=value)

    ## input dropdown data ##
    for key, value in dropdown_dict.items():
        ta.select_dropdown(element_id=key, value=value)

    ## Tick on message to all accor.com
    driver.execute_script('document.getElementById("gi.mesToHotelOnAH").checked = true;')
    
    # get response after click submit
    ta.click_button('hotelTax.submitButton')
    ta.get_response(hotel_rid, code="submitGeneralInformationForm")