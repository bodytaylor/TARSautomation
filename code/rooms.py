import time
import pyautogui
import pandas as pd
from functions import *

# Load Room Data
def load_room_data(hotel_rid):
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Roomtypes"
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=8, dtype=str)
    df = df.dropna(subset=['TARS product code'])
    df = df.dropna(axis=1, how='all')
    df = df.drop(columns=['Unnamed: 1'])
    df = df.reset_index(drop=True)
    df = df.drop(index=0)
    columns_to_drop = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(columns=columns_to_drop)
    # to remove in case of error use this line below replace with row number to start
    # df = df.drop(df.index[0:13])
    return df

def add(hotel_rid):
    # set file path and url
    url = 'https://dataweb.accor.net/dotw-trans/productTabs!input.action'

    # open url and load excel file
    open_web(url)          
    # import room data for seach in the menu

    excel_file = 'room_library.xlsx'
    room_df = pd.read_excel(excel_file)

    # function for finding room category
    def get_category_by_code(df, code):
        matching_categories = df[df['code'] == code]['category'].tolist()
        return matching_categories

    try:
        # Load Excel file and select the sheet
        room_data = load_room_data(hotel_rid)
        print(room_data)
        
            # loop until room code is none
            # Default Value is 11
        i = 0
        previous_search = ''
        for index, row in room_data.iterrows():
            # locate a menu and search for room type
            room_code = str(row['TARS product code']).strip()
            # Check Room Code
            category = get_category_by_code(room_df, code=room_code)[0]
                    
            # locate products menus tab
            locate_product_menu()
                
            # check previous search
            if previous_search != category:
                product_search(product_type=category)
                
            # Search for room code
            code_search(room_code)
            find_add()
            time.sleep(2)
            # Add data
                    
            # tick on site or close by -> Room always onsite 7 times to this section
            find_and_click_on('img\\add_product.PNG')
            tabing(4)
                
            # paying product tickbox
            pyautogui.press('space')
            tabing(1)
                
            # book abble product tickbox
            pyautogui.press('space')
            tabing(1)           
                    
            # Web only tickbox = skip this one 
            tabing(1)
                    
            # Max Occupency 
            max_occ = str(row['Maximum occupancy *']).strip()
            pyautogui.write(max_occ)
            tabing(1)
                    
            # Adult
            adult = str(row['Maximum adults *']).strip()
            pyautogui.write(adult)
            tabing(1)
                    
            # Children
            children = str(row['Maximum children *']).strip()
            pyautogui.write(children)
            tabing(1)
                    
            # Nb of beds for 1 pax
            bed_for_1 = str(row['Nb of bed available for\n1 pax *']).strip()
            pyautogui.write(bed_for_1)
            tabing(1)          
                    
            # Nb of beds for 2 pax
            bed_for_2 = str(row['Nb of bed available for\n2 pax *']).strip()
            pyautogui.write(bed_for_2)
            tabing(1)       
                        
            # room size
            room_size = str(row['Room size m²*']).strip()
            pyautogui.write(room_size)
            tabing(2) 
                    
            # Quantity of product
            quantity = str(row['Quantity\nof product *']).strip()
            pyautogui.write(quantity)
            tabing(1) 
                    
            # PMS product code -> Put room code
            pyautogui.write(room_code)
            tabing(1)
                    
            # Available on GDS and Media (always tick)
            pyautogui.press('space')
            tabing(1)
                    
            # Order in RESA Screen 
            order_resa = str(row['Order \nin resa \nscreen *'])
            pyautogui.write(order_resa)
            tabing(1)
                    
            # Max quantity of the product in room -> skip
            tabing(1)
                    
            # Click add
            pyautogui.press('enter')
            time.sleep(2)
                    
            # Print the result
            print(f'{room_code} was added successfully!')
                    
            i += 1

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        print('All Rooms was added to TARS!')
        print('Next Step Room discription and translation')