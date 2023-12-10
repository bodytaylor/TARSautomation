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
    driver.get("https://dataweb.accor.net/dotw-trans/secure/guaranteeTabs!input.action")
    wait_element(element_id='allGuaranteesTabLink')

    # Let Rolls!
    tars_response = []
    guarantees_list = ['AX','CA', 'VI', 'WIRE', 'IATA', 'PCHECK', 'CASH', 'CCHECK', 'PREP1', 'GTO']
    for item in guarantees_list:
        add_element(item)
        if item == 'IATA':
            tick_box_select('hotelGuarantee.qualified')
        if item not in ['PCHECK', 'CCHECK']:
            tick_box_select('hotelGuarantee.availableOnGDSMedia')
        click_on_element('hotelGuarantee.submitButton')
        get_response(driver=driver, code=item, response=tars_response)
        
    # Print mission report to user
    for item in tars_response:
        print(f'{hotel_rid}: {item}')
        