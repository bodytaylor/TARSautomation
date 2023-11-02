from functions import *

def add(hotel_rid):
    # Get Email from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    email = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['C45'], 
        sheet_name='Address&Setup'
    )[0]

    # Find web browser and webbrowser console that already opened
    find_edge_console()
    go_to_url('https://dataweb.accor.net/dotw-trans/displayDistribMethod!input.action')
    time.sleep(2)

    # Fill form
    select_1 = 'var selectElement = document.getElementById("hotTransmissionPartner.standardPartner.type"); selectElement.value = "B";'
    select_2 = 'var selectElement = document.getElementById("hotTransmissionPartner.recoveryPartner.type"); selectElement.value = "B";'

    order = [select_1, select_2]
    time.sleep(1)
    find_logo()
    for i in order:
        type_and_enter(i)
        time.sleep(0.25)
        
    time.sleep(1)

    add_email = 'addAddressMessage()'
    select_email = 'document.getElementById("mediaTypesEM").checked = true;'
    enter_email = f'document.getElementById("addressMessageAddress").value = "{email}";'
    click_update ='document.getElementById("addressMessage.modifyButton").click();'
    update = 'var buttonElement = document.getElementById("addressMessage.updateButton"); if (buttonElement) { buttonElement.onclick(); }'

    order = [add_email, select_email, enter_email, click_update, update]
    find_logo()
    for i in order:
        type_and_enter(i)
        time.sleep(0.25)
        
    time.sleep(1)

    select_gn = 'var selectElement = document.getElementById("hotel.reservationDistributionMethod.code"); selectElement.value = "GN";'
    send_update = 'document.getElementById("distribMethod.submitButton").click();'

    order = [select_gn, send_update]
    find_logo()
    for i in order:
        type_and_enter(i)
        time.sleep(0.25)
        
    print(f'Distribution Method setup for {hotel_rid} is done!')