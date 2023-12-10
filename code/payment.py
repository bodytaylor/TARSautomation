from functions import *
from dictionary import *
from web_driver_init import *


# input textbox
def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.5)

# Click Add
def add_element(element):
    driver.execute_script(f"addBasicElement('{element}');")
    time.sleep(0.5)

# tick box
def tick_box_select(element_id):
    driver.execute_script(f'document.getElementById("{element_id}").checked = true;')
    time.sleep(0.5)
    
# Click on element
def click_on_element(element_id):
    driver.execute_script(f'document.getElementById("{element_id}").click();')
    time.sleep(0.5)

# Wait for element to load before continue the program
def wait_element(element_id, wait_time=10):
    WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located((By.ID, f"{element_id}"))
        )

def add(hotel_rid):
    # Goto Target URL
    driver.get("https://dataweb.accor.net/dotw-trans/secure/displayHotelPayments.action")
    wait_element(element_id='paymentsTabs')

    response = []
    # Let Rolls!
    payment_list = ['AX', 'CA', 'VI', 'WIRE', 'CREDIT', 'PCHECK', 'CR', 'CCHECK', 'PREPA1', 'PRCARD']
    for item in payment_list:
        add_element(item)
        if item not in ['CCHECK', 'PREPA1', 'PRCARD']:
            tick_box_select('hotelPaymentForm_hotelPayment_availableOnGdsOrMedias')
        click_on_element('addButton')
        get_response(driver=driver, code=item, response=response)
        
    # Print mission report to user
    for item in response:
        print(f'{hotel_rid}: {item}')