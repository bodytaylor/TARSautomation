from functions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver

def add(hotel_rid):
    # Get Email from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    email = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['C45'], 
        sheet_name='Address&Setup'
    )[0]

    # Goto target URL
    driver.get('https://dataweb.accor.net/dotw-trans/displayDistribMethod!input.action')
    element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h2'))
        )
    print(element.text)

    # Fill form
    select_1 = 'var selectElement = document.getElementById("hotTransmissionPartner.standardPartner.type"); selectElement.value = "B";'
    select_2 = 'var selectElement = document.getElementById("hotTransmissionPartner.recoveryPartner.type"); selectElement.value = "B";'

    order = [select_1, select_2]
    time.sleep(1)
    for i in order:
        driver.execute_script(i)
        time.sleep(0.25)
        
    time.sleep(1)

    add_email = 'addAddressMessage()'
    select_email = 'document.getElementById("mediaTypesEM").checked = true;'
    enter_email = f'document.getElementById("addressMessageAddress").value = "{email}";'
    click_update ='document.getElementById("addressMessage.modifyButton").click();'
    update = 'var buttonElement = document.getElementById("addressMessage.updateButton"); if (buttonElement) { buttonElement.onclick(); }'

    order = [add_email, select_email, enter_email, click_update, update, click_update]
    for i in order:
        driver.execute_script(i)
        time.sleep(0.25)
    action_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'actionMessage'))
        )
    print(f'[INFO] - {action_message.text}')

    select_gn = 'var selectElement = document.getElementById("hotel.reservationDistributionMethod.code"); selectElement.value = "GN";'
    send_update = "submitDistribMethodForm ($('distributionMethod'));"

    order = [select_gn, send_update]
    time.sleep(2)
    for i in order:
        driver.execute_script(i)
        time.sleep(0.25)
    action_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'actionMessage'))
        )
    print(f'[INFO] - {action_message.text}')
        
    print(f'Distribution Method setup for {hotel_rid} is done!')