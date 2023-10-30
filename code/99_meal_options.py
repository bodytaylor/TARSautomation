import time
import pandas as pd
from functions import *

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

find_console()

# mandatory meal option
meal_options_list = ['MPHB', 'AMPHB', 'DMPHB', 'PACKAI', 'APACKA', 'DPACKA']

hotel_list = []

for item in hotel_list:
    pyautogui.hotkey('ctrl', 'l')
    type_and_enter(f'document.getElementById("codeHotel").value = "{item}";')
    type_and_enter('''document.querySelector('a[title="Launch quick change"]').click();''')
    find_logo()
    time.sleep(3)

    # start Loop!
    for item in meal_options_list:
        pyautogui.hotkey('ctrl', 'l')
        add = (add_product(item, df=product_lib_df))
        type_and_enter(add)
        time.sleep(1.5)
    # Meal is paying product
        tick_box(element='hotelProduct.paying')
        input_textf(element_id='hotelProduct.maxOccupancyTotal', text='1')
        time.sleep(0.5)
        input_textf(element_id='hotelProduct.maxQtyInRoom', text='1')
        time.sleep(0.5)
        input_textf(element_id='hotelProduct.orderInResaScreen', text='99')
        time.sleep(0.5)
        input_textf(element_id='hotelProduct.maxOccupancyAdult', text='1')
        time.sleep(0.5)
        tick_box(element='hotelProduct.availableOnGDSMedia')
        time.sleep(0.5)
        type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
        print(f'INFO - {item} has been added')
        time.sleep(2)
        

