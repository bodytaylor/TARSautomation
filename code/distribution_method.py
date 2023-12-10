import TarsAutomation as ta
from TarsAutomation import driver
import time

def add(hotel_rid, hotel_content):
    email = hotel_content.hotel_email
    # Goto target URL
    ta.get('https://dataweb.accor.net/dotw-trans/displayDistribMethod!input.action')
   
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

    order = [add_email, select_email, enter_email, click_update, update]
    for i in order:
        driver.execute_script(i)
        time.sleep(0.25)
    ta.get_response(hotel_rid)

    select_gn = 'var selectElement = document.getElementById("hotel.reservationDistributionMethod.code"); selectElement.value = "GN";'
    send_update = "submitDistribMethodForm ($('distributionMethod'));"

    order = [select_gn, send_update]
    time.sleep(2)
    for i in order:
        driver.execute_script(i)
        time.sleep(0.25) 
    ta.get_response(hotel_rid)
    
    print(f'Distribution Method setup for {hotel_rid} is done!')