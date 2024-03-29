import csv
from datetime import date
from TarsAutomation import logger

# In the future add fuction
# Check region of the hotel if hotel located in Pacific use MS instead of MC.

def add(hotel_rid, hotel_content):
    # Create dict for mandatory program to load
    mandatory_program = {
        'TR': hotel_rid,
        'CC': f'ACC{hotel_rid}',
        'DP': hotel_rid,
        'PP': hotel_rid,
        'PC': hotel_rid,
        'LE': hotel_rid,
        'IP': hotel_rid,
        'MC': hotel_rid,
        'RT': hotel_rid,
        'SA': hotel_rid,
        'AS': 1,
        'UC': hotel_rid
    }

    # hotel segmentation
    premium_luxury = [
        '21c MUSEUMHOTELS', '25HOURS', 'ADAGIO PREMIUM', 'ANGSANA', 'ART SERIES', 'BANYAN TREE',
        'DHAWA', 'FAENA', 'FAIRMONT', 'GRAND MERCURE', 'HYDE', 'MGALLERY BY SOFITEL', 'MONDRIAN',
        'MORGANS ORIGINALS', 'MOVENPICK', 'MOVENPICK LIVING', 'PEPPERS', 'PULLMAN', 'RAFFLES',
        'RIXOS HOTELS', 'SLS', 'SO SOFITEL', 'SOFITEL', 'SOFITEL LEGEND', 'SWISSOTEL', 
        'SWISSOTEL LIVING', 'THE SEBEL'
    ]

    # Create loading dict
    loading_dict = mandatory_program

    # assign for condition check
    brand = hotel_content.brand
    country = hotel_content.country
    gps = hotel_content.gps
    
    # Get Restaurant information if resturant is in the property will load dinning offer.
    restaurant = hotel_content.restaurants

    # Condition Check and Add to loading dict

    # Hidden member rate
    if brand == 'RAFFLES':
        loading_dict['NC'] = hotel_rid
        
    # TARS with out ORS
    include_brands_hb = ['RAFFLES', 'FAIRMONT', 'SWISSOTEL']
    if brand in include_brands_hb:
        loading_dict['HB'] = hotel_rid

    # GPS if state No load it
    if gps == 'NO':
        loading_dict['GP'] = 'No Distribution'

    # Booking with point
    # not participate brands
    non_bu_brands = ['MANTRA', 'PEPPERS', 'BREAKFREE', 'ART SERIES', 'HOTELF1', 'IBIS BUDGET']
    non_bu_brands_cn = ['IBIS HOTELS', 'IBIS STYLES',]

    if brand not in non_bu_brands:
        if country == 'CHINA' and brand not in non_bu_brands_cn:
            loading_dict['BU'] = hotel_rid
        elif country != 'CHINA':
            loading_dict['BU'] = hotel_rid
    elif (brand == 'IBIS BUDGET') and (country == 'BRAZIL'):
        loading_dict['BU'] = hotel_rid
        print('load bu 2')

    non_el = 'HOTELF1'
    non_el_cn = ['IBIS HOTELS', 'IBIS STYLES', 'IBIS BUDGET']

    # All enrollment check
    if brand not in non_el:
        if country == 'CHINA' and brand not in non_el_cn:
            loading_dict['EL'] = hotel_rid
        elif country != 'CHINA':
            loading_dict['EL'] = hotel_rid

    # Complimentary BF
    non_com_bf = ['IBIS BUDGET', 'HOTELF1']
    non_com_bf_cn = ['IBIS HOTELS', 'IBIS STYLES']
    if brand not in non_com_bf:
        if country == 'CHINA' and brand not in non_com_bf_cn:
            loading_dict['CO'] = hotel_rid
        elif country != 'CHINA':
            loading_dict['CO'] = hotel_rid

    # Suit night Upgrade
    if brand in premium_luxury:
        loading_dict['SU'] = hotel_rid
        
    # Dining and SPA
    if restaurant != None:
        loading_dict['DL'] = hotel_rid

    # Get current day data
    today = date.today()

    # Create list to match file templete
    rows = []
    for key, value in loading_dict.items():
        row = {
            'Action': 'A',
            'HRID': f'H{hotel_rid}',
            'Program Code': key,
            'Identification': value,
            'Hotel Contact': '',
            'Contract Date': today.strftime("%Y%m%d")
        }
        
        rows.append(row)

    # Write to csv file inside hotel folder
    csv_path = f'hotel_workbook\{hotel_rid}\H{hotel_rid}_Hotel_Programs_REG.csv'

    with open(csv_path, 'w', newline='') as csvfile:
        header = ['Action', 'HRID', 'Program Code', 
                    'Identification', 'Hotel Contact', 'Contract Date']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
        
    # End of the program
    logger.info(f'H{hotel_rid}_Hotel_Programs_REG.csv has been created!')
    print('Please upload it in Hotel Distribution -> Automate Upload\n-> Hotel Programs Registration\n')
    