import pyautogui
from functions import *

# Function to count even rows until an empty cell is encountered
def count_rows(sheet, column_letter, start_row):
    row_count = 0
    row = start_row
    
    while True:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            break
        if cell_value is not None:
            row_count += 1
        row += 4
    
    return row_count

# format time object to str
def format_time(time):
    return time.strftime("%H:%M") if time is not None else ""

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Load workbook and read the data
excel_file_path = f'TARSautomation\hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Restaurant"  
restaurants = {}
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Count even rows
        row_count = count_rows(sheet, "B", 15)
        print(f"Content book contain: {row_count} item(s)")

        # Loop through the rows and enter data
        cell_start = 15
        for i in range(row_count):
            # Get data from excel file
            # rank = i
            rank = i + 1
            
            # Restuarant name
            rt_name = sheet[f"B{cell_start}"].value
            
            # Opening Hours information
            morning_open = sheet[f"L{cell_start}"].value
            morning_close = sheet[f"M{cell_start}"].value
            evening_open = sheet[f"N{cell_start + 1}"].value
            evening_close = sheet[f"O{cell_start + 1}"].value

            # format time object with function
            morning_open_formatted = format_time(morning_open)
            morning_close_formatted = format_time(morning_close)
            evening_open_formatted = format_time(evening_open)
            evening_close_formatted = format_time(evening_close)

            # condition for write open time
            if not morning_open and not morning_close and not evening_open and not evening_close:
                open_hour = ""
            elif not evening_open and not evening_close:
                open_hour = f'{morning_open_formatted}-{morning_close_formatted}'
            elif not morning_open and not morning_close:
                open_hour = f'{evening_open_formatted}-{evening_close_formatted}'
            elif not morning_close and not evening_open:
                open_hour = f'{morning_open_formatted}-{evening_close_formatted}'
            else:
                open_hour = f'{morning_open_formatted}-{morning_close_formatted}/{evening_open_formatted}-{evening_close_formatted}'

            # Cooking Type Dropdown
            cook_type = sheet[f"P{cell_start}"].value
            
            # Open information Tickbox
            mid_mon = sheet[f"E{cell_start}"].value
            mid_tue = sheet[f"F{cell_start}"].value
            mid_wed = sheet[f"G{cell_start}"].value
            mid_thu = sheet[f"H{cell_start}"].value 
            mid_fri = sheet[f"I{cell_start}"].value
            mid_sat = sheet[f"J{cell_start}"].value
            mid_sun = sheet[f"K{cell_start}"].value
            eve_mon = sheet[f"E{cell_start + 1}"].value
            eve_tue = sheet[f"F{cell_start + 1}"].value
            eve_wed = sheet[f"G{cell_start + 1}"].value
            eve_thu = sheet[f"H{cell_start + 1}"].value 
            eve_fri = sheet[f"I{cell_start + 1}"].value
            eve_sat = sheet[f"J{cell_start + 1}"].value
            eve_sun = sheet[f"K{cell_start + 1}"].value

            # Payment Option Tickbox
            cash =          sheet[f"R{cell_start}"].value
            credit_card =   sheet[f"S{cell_start}"].value
            check =         sheet[f"T{cell_start}"].value
            other =         sheet[f"U{cell_start}"].value

            # Chef -> skip
            
            # price -> skip
            
            # Max seats
            max_seats = sheet[f"Q{cell_start}"].value
            if max_seats == None:
                max_seats = 0
                
            # Service option
            full_board =    sheet[f"V{cell_start}"].value
            half_board =    sheet[f"W{cell_start}"].value
            wheel_chair =   sheet[f"X{cell_start}"].value
            air_con =       sheet[f"Y{cell_start}"].value
            smoking =       sheet[f"Z{cell_start}"].value
            view =          sheet[f"AA{cell_start}"].value
            thematic =      sheet[f"AB{cell_start}"].value
            meal_pool =     sheet[f"AC{cell_start}"].value
            pet_allow =     sheet[f"AD{cell_start}"].value
            terrace =       sheet[f"AE{cell_start}"].value
            
            # Classifications & labels -> tickbox
            michelin_1 =    sheet[f"AF{cell_start}"].value
            michelin_bib =  sheet[f"AI{cell_start}"].value
            michelin_2 =    sheet[f"AG{cell_start}"].value
            aaa_guide =     sheet[f"AJ{cell_start}"].value
            michelin_3 =    sheet[f"AH{cell_start}"].value
            
            # Menus -> tickbox
            children =      sheet[f"AK{cell_start}"].value
            salt_free =     sheet[f"AL{cell_start}"].value
            delight =       sheet[f"AM{cell_start}"].value
            vegetarian =    sheet[f"AN{cell_start}"].value
            halal =         sheet[f"AQ{cell_start}"].value
            brunch =        sheet[f"AO{cell_start}"].value
            gluten_free =   sheet[f"AP{cell_start}"].value
            kosher =        sheet[f"AR{cell_start}"].value
            
            # Ongoing Service -> skip
            
            # Parameter for central use -> skip
    
            # add to dict
            restaurants[rt_name] = [{'open_hour': open_hour},
                                    {'rank': rank},
                                    {'cook_type': cook_type},
                                    {'Open information': [
                                        mid_mon,
                                        mid_tue,
                                        mid_wed,
                                        mid_thu, 
                                        mid_fri, 
                                        mid_sat, 
                                        mid_sun, 
                                        eve_mon, 
                                        eve_tue, 
                                        eve_wed, 
                                        eve_thu, 
                                        eve_fri, 
                                        eve_sat, 
                                        eve_sun 
                                        ]},
                                    {'Payment Option': [
                                        cash,
                                        credit_card,
                                        check,
                                        other       
                                        ]},
                                    {'Max seats': max_seats},
                                    {'Service option': [
                                        full_board,
                                        half_board, 
                                        wheel_chair,
                                        air_con,
                                        smoking ,
                                        view,
                                        thematic,
                                        meal_pool,
                                        pet_allow,
                                        terrace
                                        ]},
                                    {'Classifications': [
                                        michelin_1,
                                        michelin_bib,
                                        michelin_2,
                                        aaa_guide,
                                        michelin_3 
                                        ]},
                                    {'Menus': [
                                        children,
                                        salt_free,
                                        delight,
                                        vegetarian,
                                        halal,
                                        brunch,
                                        gluten_free,
                                        kosher
                                    ]}
                                    ]

            cell_start += 4

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close()

# Open web browser
url = 'https://dataweb.accor.net/dotw-trans/restaurantTabs!input.action'
open_web(url)

# Locate menu and reorder search result
tabing(2)
pyautogui.press('enter')
find_and_click('TARSautomation\\img\\type_code.PNG')
find_searchbox()
pyautogui.write('rt')
pyautogui.press('enter')

# Start Looping!
for keys in restaurants:
    
    # Find add button and start entering data
    find_add()
    time.sleep(1)
    find_and_click_on('TARSautomation\\img\\add_res.PNG')
    tabing(2)
    
    # Enter Ranking
    rank = str(restaurants[f'{keys}'][1]['rank'])
    pyautogui.write(rank)
    tabing(6)
    
    # Enter name of the restaurant
    pyautogui.write(keys)
    tabing(1)
    
    # Enter Opening hour
    pyautogui.write(restaurants[f'{keys}'][0]['open_hour'])
    tabing(1)
    
    # Enter Cooking style
    loop_key_press(restaurants[f'{keys}'][2]['cook_type'])
    tabing(1)
    
    # Tickbox Open Information
    tickbox(data=restaurants[f'{keys}'][3]['Open information'])
    
    # Tickbox Payment Information
    tickbox(data=restaurants[f'{keys}'][4]['Payment Option'])
    
    # Skip Ex Chef & Skip AVG price
    tabing(2)
    
    # Enter Max Seats
    max_pax = str(restaurants[f'{keys}'][5]['Max seats'])
    pyautogui.write(max_pax)
    tabing(1)
    
    # Tickbox Service option
    tickbox(data=restaurants[f'{keys}'][6]['Service option'])
    
    # Tickbox Classifications & labels
    tickbox(data=restaurants[f'{keys}'][7]['Classifications'])
    
    # Menus
    tickbox(data=restaurants[f'{keys}'][8]['Menus'])
    
    # Find Update Button
    tabing(11)
    pyautogui.press('enter')
    print(f'Restaurant {keys} has been added!')
    
    # Wait page to load and locate menu again
    find_logo()
    tabing(2)
    pyautogui.press('enter')
    time.sleep(1)
    
    
print(f'All restaurants has been loaded to {hotel_rid}!')
print("don't forget to add description!")
