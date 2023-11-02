import time
import pyautogui
from functions import *
from dictionary import *

# input textbox
def input_text(element_id, text):
    pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
    time.sleep(0.5)
    pyautogui.press('enter')
    
# select dropdown
def select_dropdown(element_id, value):
    pyautogui.typewrite(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
    time.sleep(0.5)
    pyautogui.press('enter')

# Starting point    
def add(hotel_rid):

    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['C4', 'C6', 'J6', 'D32', 'K10', 'C34', 'J34', 'C37', 'J39', 'K43', 'K45', 'C47', 'K37', 'C41', 'C45', 'C49', 'C39', 'D41', 'D43'], 
        sheet_name='Address&Setup'
    )

    # Hotel name C4
    hotel_name = data[0]

    # Brand C6
    brand = data[1]
    brand_key = search_key(brands_dict, brand)

    # Chain J6
    chain = data[2]
    chain_key = search_key(chian_dict, chain)

    # Hotel Commercial Brand D32
    hotel_com_name = data[3]

    # Provisional Opening date merge with commercial name K10
    open_date = data[4]
    open_date = open_date.strftime("%B %Y")
    print(open_date)
    hotel_com_name = f'{hotel_com_name} (Opening {open_date})'


    # Short name -> Ask User
    print(f"Hotel Commercial name: {hotel_com_name}")

    while True:
        short_name = str(input(f"Please Specify Hotel Short Name: ")).upper()
        
        if len(short_name) > 21:
            print("Please shorten the hotel name! Make it less than 22 characters.")
        
        if len(short_name) <= 21:
            break
        
    print(f'Hotel Short name: {short_name}')

    # Address line 1 2 3 -> C34 J34 C37
    address1 = data[5]
    address2 = data[6]
    address3 = data[7]

    # City: C39
    city = data[16]

    # State for country with state - if None skip J39
    state = data[8]

    # IATA city code -> Manual GDS Emulator -> Ask User
    iata = str(input("Please Check hotel city location in GDS Emulator and Enter it here: "))
    iata = iata.upper()

    # Phone D41
    phone = data[17]

    # Resa Phone K43
    resa_phone = data[9]

    # Fax D43
    fax = data[18]

    # Resa Fax K45
    resa_fax = data[10]

    # logging Type C47
    logging = data[11]
    logging_key = search_key(loggin_type_dict, logging)

    # Zipcode K37
    zipcode = data[12]

    # Phone Country code: C41
    phone_country_code = data[13]

    # Segment -> Tracking always
    # TARS mode Select -> Offline
    # PMS interface -> None

    # Email C45
    email = data[14]

    # Code place: C49
    code_place = data[15]

    # internet Access -> all.accor.com/rid
    inter_acc = f'all.accor.com/{hotel_rid}'

    # Tell user to open web console


    # Goto Target URL
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')
    time.sleep(2)

    # Fill data in console
    # Hotel name
    input_textf(element_id="hotel.name", text=hotel_name)

    # Select Brand
    select_dropdownf(element_id="hotel.brand.code", value=brand_key)

    # Select Chain
    select_dropdownf(element_id="hotel.chain.code", value=chain_key)

    # Hotel Commercial name
    input_textf(element_id="hotel.commercialName", text=hotel_com_name)

    # Hotel Short Name
    input_textf(element_id="hotel.shortName", text=short_name)

    # logging type
    select_dropdownf(element_id="hotel.hotelManagementType.code", value=logging_key)

    # Address 1 2 3
    if address1 != None:
        input_textf(element_id="hotel.address.addresses[0]", text=address1)
    if address2 != None:    
        input_textf(element_id="hotel.address.addresses[1]", text=address2)
    if address3 != None:
        input_textf(element_id="hotel.address.addresses[2]", text=address3)

    # City
    input_textf(element_id="hotel.address.city", text=city)

    # State
    if state != None:
        print('Please Select State by your self, Thanks!')
        
    # IATA City Code
    input_textf(element_id="hotel.iataCityCode", text=iata)

    # Zipcode
    input_textf(element_id="hotel.address.zipCode", text=zipcode)

    # Phone and Fax
    input_textf(element_id="hotel.address.indTel", text=phone_country_code)
    input_textf(element_id="hotel.address.tel", text=phone)
    input_textf(element_id="hotel.address.indFax", text=phone_country_code)
    input_textf(element_id="hotel.address.fax", text=fax)

    # Resa Phone and Resa Fax
    input_textf(element_id="hotel.indTelReservation", text=phone_country_code)
    input_textf(element_id="hotel.telReservation", text=resa_phone)
    input_textf(element_id="hotel.indFaxReservation", text=phone_country_code)
    input_textf(element_id="hotel.faxReservation", text=resa_fax)

    # Hotel Code Place
    input_textf(element_id="hotel.placeCode", text=code_place)

    # Tracking
    select_dropdownf(element_id="hotel.segmentationType.code", value="TRACK")

    # TARS Mode
    select_dropdownf(element_id="hotel.tarsMode.code", value="O")

    # PMS interface
    select_dropdownf(element_id="versionPmsInterface", value="")

    # Email
    input_textf(element_id="hotel.address.email", text=email)

    # Internet Address
    input_textf(element_id="hotel.internetAddress", text=inter_acc)

    # Run code

    print('Automation Done Please Review The input data before click save! Thanks.')
