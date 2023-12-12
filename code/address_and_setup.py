import TarsAutomation as ta
from TarsAutomation import driver, logger
from dictionary import *

# Starting point    
def add(hotel_rid, hotel_content):
    # Hotel name C4
    hotel_name = hotel_content.hotel_name
    
    # Brand C6
    brand = hotel_content.brand
    brand_key = search_key(brands_dict, brand)

    # Chain J6
    chain = hotel_content.chain
    chain_key = search_key(chian_dict, chain)

    # Hotel Commercial Brand D32
    hotel_com_name = hotel_content.hotel_commercial_name

    # Provisional Opening date merge with commercial name K10
    open_date = hotel_content.open_date
    open_date = open_date.strftime("%B %Y")
    hotel_com_name = f'{hotel_com_name} (Opening {open_date})'


    # Short name -> Ask User
    print(f"Hotel Commercial Name: {hotel_com_name}")

    while True:
        short_name = str(input(f"Please Specify Hotel Short Name: ")).upper()
        
        if len(short_name) > 21:
            print("Please shorten the hotel name! Make it less than 22 characters.")
        
        if len(short_name) <= 21:
            break
        
    print(f'Hotel Short name: {short_name}')

    # Address line 1 2 3 -> C34 J34 C37
    address1 = hotel_content.address1
    address2 = hotel_content.address2
    address3 = hotel_content.address3

    # City: C39
    city = hotel_content.city

    # State for country with state - if None skip J39
    state = hotel_content.state

    # IATA city code -> Manual GDS Emulator -> Ask User
    iata = str(input("Please Check hotel city location in GDS Emulator and Enter it here: "))
    iata = iata.upper()

    # Phone D41
    phone = hotel_content.phone

    # Resa Phone K43
    resa_phone = hotel_content.resa_phone

    # Fax D43
    fax = hotel_content.fax

    # Resa Fax K45
    resa_fax = hotel_content.resa_fax

    # logging Type C47
    logging = hotel_content.logging_type
    logging_key = search_key(loggin_type_dict, logging)

    # Zipcode K37
    zipcode = hotel_content.zip_code

    # Phone Country code: C41
    phone_country_code = hotel_content.phone_country_code

    # Segment -> Tracking always
    # TARS mode Select -> Offline
    # PMS interface -> None

    # Email C45
    email = hotel_content.hotel_email

    # Code place: C49
    code_place = hotel_content.code_place

    # internet Access -> all.accor.com/rid
    inter_acc = f'all.accor.com/{hotel_rid}'

    # Country
    country = hotel_content.country
    country_code = country_dict.get(country)

    # Goto Target URL
    ta.get('https://dataweb.accor.net/dotw-trans/displayHotelAddress!input.action')
    
    # Fill data in console
    # Hotel name
    ta.input_text(element_id="hotel.name", text=hotel_name)

    # Select Brand
    ta.select_dropdown(element_id="hotel.brand.code", value=brand_key)

    # Select Chain
    ta.select_dropdown(element_id="hotel.chain.code", value=chain_key)

    # Hotel Commercial name
    ta.input_text(element_id="hotel.commercialName", text=hotel_com_name)

    # Hotel Short Name
    ta.input_text(element_id="hotel.shortName", text=short_name)

    # logging type
    ta.select_dropdown(element_id="hotel.hotelManagementType.code", value=logging_key)

    # Address 1 2 3
    if address1 != None:
        ta.input_text(element_id="hotel.address.addresses[0]", text=address1)
    if address2 != None:    
        ta.input_text(element_id="hotel.address.addresses[1]", text=address2)
    if address3 != None:
        ta.input_text(element_id="hotel.address.addresses[2]", text=address3)

    # City
    ta.input_text(element_id="hotel.address.city", text=city)

    # State
    if state != None:
        print('Please Select State by your self, Thanks!')
        
    # IATA City Code
    ta.input_text(element_id="hotel.iataCityCode", text=iata)

    # Zipcode
    ta.input_text(element_id="hotel.address.zipCode", text=zipcode)

    # Phone and Fax
    ta.input_text(element_id="hotel.address.indTel", text=phone_country_code)
    ta.input_text(element_id="hotel.address.tel", text=phone)
    ta.input_text(element_id="hotel.address.indFax", text=phone_country_code)
    ta.input_text(element_id="hotel.address.fax", text=fax)

    # Resa Phone and Resa Fax
    ta.input_text(element_id="hotel.indTelReservation", text=phone_country_code)
    ta.input_text(element_id="hotel.telReservation", text=resa_phone)
    ta.input_text(element_id="hotel.indFaxReservation", text=phone_country_code)
    ta.input_text(element_id="hotel.faxReservation", text=resa_fax)
    
    # Select Country
    ta.select_dropdown(element_id="hotel.address.country.code", value=country_code)

    # Hotel Code Place
    ta.input_text(element_id="hotel.placeCode", text=code_place)

    # Tracking
    ta.select_dropdown(element_id="hotel.segmentationType.code", value="TRACK")

    # TARS Mode
    ta.select_dropdown(element_id="hotel.tarsMode.code", value="O")

    # PMS interface
    ta.select_dropdown(element_id="versionPmsInterface", value="")

    # Email
    ta.input_text(element_id="hotel.address.email", text=email)

    # Internet Address
    ta.input_text(element_id="hotel.internetAddress", text=inter_acc)

    # Update and get response
    ta.driver.execute_script("submitHotelAddressForm ('updateHotelAddress.action');")
    ta.get_response(hotel_rid, code='updateHotelAddress')
    
