import time
import pyautogui
import pandas as pd
from functions import *

# version 1.0.2
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
    # set file path and url
    url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Other Services"

    # Load excel file to Pandas Data Frame
    products_df = pd.read_excel(excel_file_path, sheet_name=sheet_name, skiprows=9)

    # Clean data
    products_df = products_df.drop(columns=['Unnamed: 0', 'Family', 'Hotel services', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
                            'Displayed on AccorHotels.com', 'Amount', 'Unnamed: 11'])
    products_df = products_df.dropna()
    products_df = products_df[products_df['Product is present\nYes/No'] != 'No']
    products_df = products_df.rename(columns={
        'Product is present\nYes/No': 'available',
        'Paying\nYes/No': 'paying'
    })

    # Load product library
    csv_path = 'products_lib.csv'
    product_lib_df = pd.read_csv(
        csv_path,
        header=0,
        sep=';'
    )

    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    time.sleep(2)

    # Start Loop
    products_not_found = []
    for index, row in products_df.iterrows():
        add = (add_product(row['Code'], df=product_lib_df))
        if add == None:
            products_not_found.append(row['Code'])
        type_and_enter(add)
        time.sleep(1)
    
        if row['paying'] == 'Yes':
            tick_box(element='hotelProduct.paying')
            input_textf(element_id='hotelProduct.maxOccupancyTotal', text='1')
            input_textf(element_id='hotelProduct.maxQtyInRoom', text='1')
            input_textf(element_id='hotelProduct.orderInResaScreen', text='99')
            input_textf(element_id='hotelProduct.maxOccupancyAdult', text='1')
        tick_box(element='hotelProduct.availableOnGDSMedia')
        
        type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
        print(f'INFO - {row} has been added')
        time.sleep(1.5)   
        
    if len(products_not_found) != 0:
        print(f'[INFOR] - Please Manually Check this product: {products_not_found}')
        
    