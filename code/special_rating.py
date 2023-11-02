import time
import pyautogui
from functions import *

def add(hotel_rid):
    # get data from excel file
    excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'

    data = get_excel_values(
        file_path=excel_file, 
        cell_addresses=['G65'], 
        sheet_name='Address&Setup'
    )

    local_rating = data[0]

    # Fill data in console
    find_edge_console()
    # walk to this url
    go_to_url("https://dataweb.accor.net/dotw-trans/displayHotelStandings!input.action")


    # input data in console
    # Click Add
    pyautogui.typewrite("addBasicElement('EU','Local star rating','Star');")
    pyautogui.press('enter')
    time.sleep(1)
    input_text(element_id="hotelStanding.nb", text=local_rating)
    click_button('maj')

    print(f'Local Star: {local_rating} Added to {hotel_rid}!')