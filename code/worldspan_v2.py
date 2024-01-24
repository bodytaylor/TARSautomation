import TarsAutomation as ta
from accor_repo import AccorRepo
import pandas as pd
import csv
import os
import time

def get_valid_worldspan_code(max_retries: int = 5) -> str:
    retries = 0
    while retries < max_retries:
        user_input = input('Input new Worldspan code: ').upper()
        if len(user_input) == 5:
            code_check = ta.check_available(code=user_input, system='tw')
            if code_check is True:
                return user_input
            else:
                print("Invalid Worldspan code. Please try again.")
        else:
            print("Worldspan code must be 5 characters long. Please try again.")

        retries += 1
        time.sleep(1)

    raise Exception("Failed to get a valid Worldspan code after multiple attempts.")

def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# Standard Dic
standard_dict = {
    "21c MUSEUM HOTELS": "LH",
    "25HOURS": "UP",
    "ADAGIO ACCESS": "MD",
    "ADAGIO ORIGINAL": "EY",
    "ADAGIO PREMIUM": "UP",
    "ALL SEASONS": "EY",
    "ANGSANA": "UP",
    "ART SERIES": "UP",
    "BANYAN TREE": "LH",
    "BREAKFREE": "EY",
    "BY MERCURE": "MD",
    "CASSIA": "MD",
    "DELANO": "MD",
    "DHAWA": "LH",
    "ETAP HOTEL": "BU",
    "FAENA": "LH",
    "FAIRMONT": "LH",
    "FOLIO": "MD",
    "GARRYA": "MD",
    "GRAND MERCURE": "UP",
    "GREET": "EY",
    "HANDWRITTEN": "MD",
    "HOMM": "MD",
    "HOTELF1": "BU",
    "HYDE": "LH",
    "IBIS BU": "BU",
    "IBIS HOTELS": "EY",
    "IBIS BUDGET": "EY",
    "IBIS STYLES": "EY",
    "JO&JOE": "BU",
    "MAMA SHELTER": "MD",
    "MANTRA": "MD",
    "MANTIS": "UP",
    "MERCURE": "MD",
    "MERCURE LIVING": "MD",
    "MGALLERY BY SOFITEL": "LH",
    "MONDRIAN": "LH",
    "MORGANS ORIGINALS": "LH",
    "Mövenpick": "UP",
    "MOVENPICK": "UP",
    "MOVENPICK LIVING": "UP",
    "NOVOTEL": "MD",
    "NOVOTEL LIVING": "MD",
    "NOVOTEL SUITES": "MD",
    "PEPPERS": "UP",
    "PULLMAN": "UP",
    "RAFFLES": "LH",
    "RIXOS HOTELS": "LH",
    "SLS": "LH",
    "SO SOFITEL": "LH",
    "SOFITEL": "LH",
    "SOFITEL LEGEND": "LH",
    "SWISSOTEL": "UP",
    "SWISSOTEL LIVING": "UP",
    "THE SEBEL": "UP",
    "TRIBE": "MD",
}

chain_code = {
    'BAN': 'BY', 
    '21C': 'EN', 
    'TWF': 'EN', 
    'DEL': 'EN', 
    'HYD': 'EN', 
    'MSH': 'EN', 
    'MOD': 'EN', 
    'TOR': 'EN', 
    'SLS': 'EN', 
    'SO': 'EN', 
    'FAR': 'FA', 
    'SOF': 'SB', 
    'MGR': 'SB', 
    'PUL': 'PU', 
    'PLL': 'PU', 
    'RAF': 'YR', 
    'RIX': 'RX', 
    'SWI': 'SL'
    }

# Update this inthe future for recent extraction!
def meal_plan(rid):
    df = pd.read_excel(r"Loading Referential - MEA APAC Hotels-LATEST.xlsx", dtype=str)
    # use first column as column name
    df.columns = df.iloc[0]
    df = df[1:]
    filtered_df = df[df['RID'] == rid]
    keep_cols = ['RID', 'EP', 'BB', 'HB', 'FB', 'AI']
    filtered_df = filtered_df.drop(columns=filtered_df.columns.difference(keep_cols))
    meal_option = []
    
    if not filtered_df['EP'].isna().any():
        meal_option.append('RO')

    if not filtered_df['BB'].isna().any():
        meal_option.append('BB')

    if not filtered_df['HB'].isna().any():
        meal_option.append('DB')

    if not filtered_df['FB'].isna().any():
        meal_option.append('FB')

    if not filtered_df['AI'].isna().any():
        meal_option.append('FP')
        
    return meal_option

if __name__ == "__main__":     
    
    # create code
    hotel_rid = input('Please Input Hotel RID: ')
    hotel_rid = hotel_rid.upper()
    amadeus = input(f'Please Input Amadeus Code for {hotel_rid}: ')

    # get accor repo
    repo = AccorRepo(hotel_rid)
    
    # Login
    ta.login()
    checkin = repo.checkin_time()
    checkout = repo.checkout_time()

    # chain
    hotel_chain = repo.hotel_brand()
    # Chain Code
    amadeus_chain_code = chain_code.get(hotel_chain)
    if amadeus_chain_code is None:
        amadeus_chain_code = 'RT'
        
    worldspan_code = amadeus_chain_code + amadeus[3:5] + amadeus[0:3]
    tars_check_code = amadeus[3:5] + amadeus[0:3]
    
    # name
    repo.get_hotel_info()
    hotel_name = repo.hotel_name
    # primary airport
    # address 1st line street name and number only
    repo.get_hotel_address()
    address_1 = repo.address1
    address_1 = str(address_1).replace('-', ' ')
    address_2 = repo.address2
    address_2 = str(address_2).replace('-', ' ')
    address_3 = repo.address3
    address_3 = str(address_3).replace('-', ' ')

    # tran (Y) if hotel check shuttle available for AER1
    # FAM PLAN (Y) if CHIPOL at H level is set
    # adress 2nd line city + country + zipcode
    city = repo.city
    country_code = repo.country_code
    zip_code = repo.post_code
    zip_code = str(zip_code).replace('-', '')
    country = repo.country

    # Checkin time format 0000
    # ST skip
    # CTRY C + 2 letters country code
    ctry = 'C' + country_code
    # POSTAL CODE is the zip code?
    # Checkout time format 0000
    # Phone 
    phone_index = repo.phone_code
    phone = repo.phone
    f_phone = str(phone_index) + str(phone)
    
    # COMM PERCENT 10
    commission = '10'
    
    # FAX 
    fax = repo.fax
    if repo.fax is not None:
        f_fax = str(phone_index) + str(fax)
    else:
        f_fax = ""
    
    # MEAL PLAN
    # TAX RATE 00 except JAPAN 0
    if country_code == 'JP':
        tax_rate = '0'
    else:
        tax_rate = '15'
    # PROPERTY TYPE CODE EY, LH, MD, UP
    brand_name = repo.brand_name
    property_type = standard_dict.get(brand_name)

    surrounding = repo.get_ref_point()
    result = surrounding[(surrounding['IndexPointCode'] == '6') & (surrounding['RefPointName'].str.len() == 3)]
    primary_airport = result['RefPointName'].values[0]
    shuttle_service = result['ShuttleService'].values[0]
    if shuttle_service == False:
        shuttle = 'N'
    else:
        shuttle = 'Y'

    address_line2 = f'{city} {country} {zip_code}'
    meal_option = meal_plan(hotel_rid)

    currency = repo.currency
    total_room = repo.total_room()

    code_check = ta.check_available(code=tars_check_code, system='tw')
    if code_check is False:
        try:
            worldspan_code = get_valid_worldspan_code()
        except Exception as e:
            print(e)
    
    # Future update if the code is not available ask user
    ta.driver.quit()

    # Check file directory
    directory_path = r"gds\worldspan"
    create_directory(directory_path)

    # write to csv
    file_path = f"gds\worldspan\{hotel_rid} Worldspan.csv"
    header = ['NAME', 'PRIM AIRPORT', 'ADDRESS', 'TRANS', 'FAM PLAN', 'ADDRESS_2', 'CHECK-IN',
            'ST', 'CNTRY', 'POSTAL CODE', 'CHECK OUT', 'PHONE', 'TELEX', 'COMM PERCENT',
            'FAX', 'RESV', 'MEAL PLAN', 'TAX RATE', 'PROPERTY TYPE CODES', 'CURR', 'TOTAL RMS',
            'RA', 'RC', 'CR', 'EX', 'EC', 'worldspan code', 'Check availability']

    with open(file_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow([hotel_name, primary_airport, address_1, shuttle, 'Y', address_line2, str(checkin),
                            '', ctry, str(zip_code), str(checkout), str(f_phone), '', '10', 
                            str(f_fax), '', meal_option, str(tax_rate), property_type, currency, total_room,
                            'K', 'K', 'K', 'K', 'K', worldspan_code, f'HHPC{worldspan_code}'])
        


