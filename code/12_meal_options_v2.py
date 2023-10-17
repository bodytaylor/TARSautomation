import time
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Load product library
csv_path = 'products_lib.csv'
product_lib_df = pd.read_csv(
    csv_path,
    header=0,
    sep=';'
)

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        element = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return element
    else:
        return None

find_edge_console()
go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
time.sleep(2)

# mandatory meal option
meal_options_list = ['MBREAK', 'MBUFF', 'DMBREA', 'AMBREA']

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
