from datetime import datetime
from functions import *
from dictionary import *

# input function in console
# input textbox
def input_text(element_id, text):
    if text != None:
        pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.5)
        pyautogui.press('enter')
    
# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        pyautogui.typewrite(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.5)
        pyautogui.press('enter')
        
# Name ACCOR Standard check
def accor_name(title, input_name, input_surname) -> str:
    name = input_name[0].upper() + input_name[1:].lower()
    surname = input_surname.upper()
    return f'{title} {name} {surname}'

# Name ACCOR Standard for single cell
def accor_format_name(title, text_input) -> str:
    if text_input != None:
        words = text_input.split()
        formatted_name = words[0].capitalize()
        for word in words[1:]:
            formatted_name += " " + word.upper()
        title = title.replace(".", "")
        return f'{title} {formatted_name}'
    else:
        return None
    

# Ask user for RID    
hotel_rid = str(input('Enter Hotel RID: '))
# Make it All Cap
hotel_rid = hotel_rid.upper()

# get data from excel file
excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

contact_data = get_excel_values(
    file_path=excel_file, 
    cell_addresses=['C12', 'D12', 'I12', 'J12', 'C15', 'D15', 'I15', 'J15', 'C18', 'D18', 
'I18', 'C21', 'D21', 'I21', 'I24', 'J24', 'C24', 'D24'], 
    sheet_name='Contact'
)

gm_data = get_excel_values(
    file_path=excel_file, 
    cell_addresses=['E53', 'J55', 'J53'], 
    sheet_name='Address&Setup'
)

# GM name
gm = accor_name(gm_data[0], gm_data[1], gm_data[2])


# Assistant Manager: C12, D12
am_title = contact_data[0]
am_name = contact_data[1]
am_formated = accor_format_name(am_title, am_name)

# Room Division Manager: I12, J12	
rm_title = contact_data[2]
rm_name = contact_data[3]
rm_formated = 	accor_format_name(rm_title, rm_name)			
			
# Reservation Manager: C15, D15
resm_title = contact_data[4]
resm_name = contact_data[5]
resm_formated = accor_format_name(resm_title, resm_name)

# Front Office Manager: I15, J15	
fom_title = contact_data[6]
fom_name = contact_data[7]
fom_formated = accor_format_name(fom_title, fom_name)		
  	
# Group reservation: C18, D18
gr_title = contact_data[8]
gr_name = contact_data[9]
gr_formated = accor_format_name(gr_title, gr_name)

# Banqueting e-mail: I18	
ban_email = contact_data[10]
		
# Banqueting Manager: C21, D21	
bm_title = contact_data[11]
bm_name = contact_data[12]
bm_formated = accor_format_name(bm_title, bm_name)

# Sales e-mail: I21	
sale_email = contact_data[13]
	
# Sales  contact: I24, J24
sale_title = contact_data[14]
sale_title = sale_title.replace(".", "")
sale_name = contact_data[15]
if sale_name != None:
    words = sale_name.split()
    sale_formated = words[0].capitalize()
    for word in words[1:]:
        sale_formated += " " + word.upper()
else:
    sale_formated = None
			
# Executive Chief: C24, D24
chef_title = contact_data[16]
chef_name = contact_data[17]
chef_formated = accor_format_name(chef_title, chef_name)

# Create Contact list of elements and input value
contact_dict ={
    "hotelContactsForm_hotelStaffManagers_generalManager_name": gm,
    "hotelContactsForm_hotelStaffManagers_reservationManager_name": resm_formated, 
    "hotelContactsForm_hotelStaffManagers_groupReservation_name": gr_formated,
    "hotelContactsForm_hotelStaffManagers_frontOffice_name": fom_formated,
    "hotelContactsForm_hotelStaffManagers_roomDivisionManager_name": rm_formated,
    "hotelContactsForm_hotelStaffManagers_assistantManager_name": am_formated,
    "hotelContactsForm_hotelStaffManagers_executiveChief_name": chef_formated,
    "hotelContactsForm_hotelStaffManagers_seminarAndBanquetingManager_name": bm_formated,
    "hotelContactsForm_hotelStaffManagers_seminarAndBanquetingManager_address_email": ban_email,
    "hotelContactsForm_marketingContact_name": sale_formated,
    "hotelContactsForm_marketingContact_title": sale_title,
    "hotelContactsForm_marketingContact_address_email": sale_email
}


# Tell user to open web console
print('Open web browser console by pressing CTRL + SHIFT + I')
find_console()

# Fill data in console
# Goto Target URL
type_and_enter(text='window.location.href = "https://dataweb.accor.net/dotw-trans/displayHotelContacts.action";')
time.sleep(2)
find_logo()

# input data in console
## input text data ##
for key, value in contact_dict.items():
    input_text(element_id=key, text=value)

## input dropdown data ##
select_dropdown(element_id="hotelContactsForm_marketingContact_function_code", value=50)
    
## Tick on message to all accor.com

print('Automation Done Please Review The input data before click save! Thanks.')