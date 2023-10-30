import time
import pandas as pd
from functions import *

# input textbox
def input_text(element_id, text):
    if text != None:
        pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.5)
        pyautogui.press('enter')
        
# Click Add
def add_element(element):
    pyautogui.typewrite(f"addBasicElement('{element}');")
    pyautogui.press('enter')
    time.sleep(0.5)

# tick box
def tick_box_select(element_id):
    pyautogui.typewrite(f'document.getElementById("{element_id}").checked = true;')
    pyautogui.press('enter')
    time.sleep(0.5)
    
# Click on
def click_on_element(element_id):
    pyautogui.typewrite(f'document.getElementById("{element_id}").click();')
    pyautogui.press('enter')
    time.sleep(0.5)

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


hotel_list = ['C1P3','C1R2','C1P1','C1I6','C1P2','C1R1','C1Q8','C1P4','C1P0','C1Q1','C1Q3',
              'C1Q7','C1P6','C1P9','C1Q2','C1Q5','C1R3','C1P7','C1N8','C1N7','C1P5','C1N6','C1Q6']

for item in hotel_list:
    press_ctrl_plus('l')
    type_and_enter(f'document.getElementById("codeHotel").value = "{item}";')
    type_and_enter('''var tdElement = document.getElementById("hotelQuickChangeLink"); var anchorElement = tdElement.getElementsByTagName("a")[0]; anchorElement.click();''')
    time.sleep(2)
    find_logo()
    press_ctrl_plus('l')
    time.sleep(1)

    # start Loop!
    payment_list = ['AX', 'CA', 'VI', 'WIRE', 'CREDIT', 'PCHECK', 'CR', 'CCHECK', 'PREPA1', 'PRCARD']
    for item in payment_list:
        add_element(item)
        if item not in ['CCHECK', 'PREPA1', 'PRCARD']:
            tick_box_select('hotelPaymentForm_hotelPayment_availableOnGdsOrMedias')
        click_on_element('addButton')
        time.sleep(1)
        

