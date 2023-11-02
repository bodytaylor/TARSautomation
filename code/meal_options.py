import time
import pandas as pd
from functions import *

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        element = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return element
    else:
        return None

def add(hotel_rid):
    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    # mandatory meal option *** Add According to Pricing book Need to Update
    meal_options_list = ['MBUFF']
    
    meal_data = get_excel_values(file_path=f'hotel_workbook\{hotel_rid}\{hotel_rid} Pricing Book.xlsx',
                                 sheet_name='Set-up table',
                                 cell_addresses=['C459',
                                                 'C460',
                                                 'C461',
                                                 'C462',
                                                 'C465',
                                                 'C466',
                                                 'C467',
                                                 'C468',
                                                 'C475']
                                 )
    # Append to meal option list
    mbreak = meal_data[0]
    mphb = meal_data[1]
    mpfb = meal_data[2]
    packai = meal_data[3]
    dmbrea = meal_data[4]
    dmphb = meal_data[5]
    dmpfb = meal_data[6]
    dpacka = meal_data[7]
    mbuff = meal_data[8]
    
    if mbreak is not None:
        meal_options_list.extend(['MBREAK', 'AMBREA'])
    if mphb is not None:
        meal_options_list.extend(['MPHB', 'AMPHB'])
    if mpfb is not None:
        meal_options_list.extend(['MPFB', 'AMPFB'])
    if packai is not None:
        meal_options_list.extend(['PACKAI', 'APACKA'])
    if dmbrea is not None:
        meal_options_list.append('DMBREA')
    if dmphb is not None:
        meal_options_list.append('DMPHB')
    if dmpfb is not None:
        meal_options_list.append('DMPFB')
    if dpacka is not None:
        meal_options_list.append('DPACKA')
    if mbuff is not None:
        meal_options_list.append('MBUFF')  
        
    # Print Data to user
    print('Meal Plan to add to the Hotel')
    print(meal_options_list)
    
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(2)
    
    # start Loop!
    for item in meal_options_list:
        add = (add_product(item, df=product_lib_df))
        type_and_enter(add)
        time.sleep(1)
    # Meal is paying product
        tick_box(element='hotelProduct.paying')
        input_textf(element_id='hotelProduct.maxOccupancyTotal', text='1')
        input_textf(element_id='hotelProduct.maxQtyInRoom', text='1')
        input_textf(element_id='hotelProduct.orderInResaScreen', text='99')
        input_textf(element_id='hotelProduct.maxOccupancyAdult', text='1')
        tick_box(element='hotelProduct.availableOnGDSMedia')
        type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
        print(f'INFO - {item} has been added')
        time.sleep(1.5)
        
    print(f'Mandatory Meal Option has been added to {hotel_rid}!')
