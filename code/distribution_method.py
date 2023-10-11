from functions import *

# user input for Hotel RID
hotel_rid = str(input('Enter Hotel RID: '))
# Make it All Cap
hotel_rid = hotel_rid.upper()

# Get Email from excel file
excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

email = get_excel_values(
    file_path=excel_file, 
    cell_addresses=['C47'], 
    sheet_name='Address&Setup'
)[0]

# Find web browser and webbrowser console that already opened
find_and_click(img_path=r'img\ielogo.PNG')
time.sleep(1)
find_and_click(img_path=r'img\console_logo.PNG')

# open target url and wait
find_and_click(img_path=r'img\ie12.PNG')
find_logo()
type_and_enter(text='window.location.href = "https://dataweb.accor.net/dotw-trans/displayDistribMethod!input.action";')


# Fill form
select_1 = 'var selectElement = document.getElementById("hotTransmissionPartner.standardPartner.type"); selectElement.value = "B";'
select_2 = 'var selectElement = document.getElementById("hotTransmissionPartner.recoveryPartner.type"); selectElement.value = "B";'

order = [select_1, select_2]
time.sleep(2)
find_logo()
find_and_click(img_path=r'img\ie12.PNG')
find_logo()
for i in order:
    type_and_enter(i)
    time.sleep(0.5)
    
time.sleep(2)

add_email = 'addAddressMessage()'
select_email = 'document.getElementById("mediaTypesEM").checked = true;'
enter_email = f'document.getElementById("addressMessageAddress").value = "{email}";'
click_update ='document.getElementById("addressMessage.modifyButton").click();'
update = 'var buttonElement = document.getElementById("addressMessage.updateButton"); if (buttonElement) { buttonElement.onclick(); }'

order = [add_email, select_email, enter_email, click_update, update]
find_logo()
for i in order:
    type_and_enter(i)
    time.sleep(0.5)
    
time.sleep(2)

select_gn = 'var selectElement = document.getElementById("hotel.reservationDistributionMethod.code"); selectElement.value = "GN";'
send_update = 'document.getElementById("distribMethod.submitButton").click();'

order = [select_gn, send_update]
find_logo()
for i in order:
    type_and_enter(i)
    time.sleep(0.5)
    
print(f'Distribution Method setup for {hotel_rid} is done!')