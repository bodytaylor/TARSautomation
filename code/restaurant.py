import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_driver_init import driver
from functions import load_excel_file
from functions import *

# java script execute
def tick_box(element, value):
    if value != None:
        driver.execute_script(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
        time.sleep(0.1)

def input_text(element_id, text):
    if text != None:
        driver.execute_script(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.1)

def select_dropdown(element_id, value):
    if value != None:
        driver.execute_script(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.1)
        
# dropdown dict
cooking_type_dict = {
    "Barbecue": "BBQ",
    "Bistro": "BISTRO",
    "Bistronomy": "BISNOM",
    "Brasserie": "BRASS",
    "Cafe": "CAFE",
    "Chinese": "CHINE",
    "Creole": "CREOLE",
    "Diabetic": "DIABET",
    "Dietary cuisine": "Dieta",
    "European": "EUROP",
    "French": "FRENCH",
    "Gourmet": "GASTRO",
    "Healthy eating": "DIET",
    "Indian": "INDIAN",
    "International": "INTERN",
    "Italian": "ITALY",
    "Japanese": "JAPAN",
    "Kosher": "KASHER",
    "Lebanese": "LEBANE",
    "Mediterranean": "MED",
    "Mexican": "MEXICA",
    "Other cooking style": "OTHER",
    "Regional": "REGION",
    "Thai": "THAI",
    "Thematic cuisine": "THEMA",
    "Vegetarian cuisine": "VEGET",
    "Wine bar": "BARVIN",
    }

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

def add(hotel_rid):

    # Load workbook and read the data
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
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
    driver.get(url)
    
    # collect error data
    error = []
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="allRestaurantsTabLink"]'))
        )
    
    # Start Looping!
    for keys in restaurants:
        # Find add button and start entering data
        driver.execute_script("addBasicElement('RT','RESTAURANT');")
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="hotelRestaurantFormJson"]'))
            )
        
        # Enter Ranking
        rank = str(restaurants[f'{keys}'][1]['rank'])
        input_text(element_id='hotelRestaurant.rank', text=rank)
        
        # Enter name of the restaurant
        input_text(element_id='hotelRestaurant.name', text=keys)
        
        # Enter Opening hour
        restaurant_hours = restaurants[f'{keys}'][0]['open_hour']
        input_text(element_id='hotelRestaurant.horaires', text=restaurant_hours)
        
        # Enter Cooking style
        cooking_style = restaurants[f'{keys}'][2]['cook_type']
        cooking_select = cooking_type_dict.get(cooking_style)
        select_dropdown(element_id='hotelRestaurant.cookType.code', value=cooking_select)
        
        # Tickbox Open Information
        opening_data = restaurants[f'{keys}'][3]['Open information']
        tick_box(element='hotelRestaurant.mondayMidday', value=opening_data[0])
        tick_box(element='hotelRestaurant.tuesdayMidday', value=opening_data[1])
        tick_box(element='hotelRestaurant.wednesdayMidday', value=opening_data[2])
        tick_box(element='hotelRestaurant.thursdayMidday', value=opening_data[3])
        tick_box(element='hotelRestaurant.fridayMidday', value=opening_data[4])
        tick_box(element='hotelRestaurant.saturdayMidday', value=opening_data[5])
        tick_box(element='hotelRestaurant.sundayMidday', value=opening_data[6])
        tick_box(element='hotelRestaurant.mondayEvening', value=opening_data[7])
        tick_box(element='hotelRestaurant.tuesdayEvening', value=opening_data[8])
        tick_box(element='hotelRestaurant.wednesdayEvening', value=opening_data[9])
        tick_box(element='hotelRestaurant.thursdayEvening', value=opening_data[10])
        tick_box(element='hotelRestaurant.fridayEvening', value=opening_data[11])
        tick_box(element='hotelRestaurant.saturdayEvening', value=opening_data[12])
        tick_box(element='hotelRestaurant.sundayEvening', value=opening_data[13])
        
        # Tickbox Payment Information
        payment_data = restaurants[f'{keys}'][4]['Payment Option']
        tick_box(element='hotelRestaurant.cash', value=payment_data[0])
        tick_box(element='hotelRestaurant.creditCard', value=payment_data[1])
        tick_box(element='hotelRestaurant.check', value=payment_data[2])
        tick_box(element='hotelRestaurant.othersLocalPaymentOptions', value=payment_data[3])
        
        # Skip Ex Chef & Skip AVG price
        
        # Enter Max Seats
        max_pax = str(restaurants[f'{keys}'][5]['Max seats'])
        input_text(element_id='hotelRestaurant.maximumSeating', text=max_pax)
        
        # Tickbox Service option
        service_data = restaurants[f'{keys}'][6]['Service option']
        tick_box(element='hotelRestaurant.fullBoard', value=service_data[0])
        tick_box(element='hotelRestaurant.halfBoard', value=service_data[1])
        tick_box(element='hotelRestaurant.wheelChairAccess', value=service_data[2])
        tick_box(element='hotelRestaurant.airConditionning', value=service_data[3])
        tick_box(element='hotelRestaurant.nonSmoking', value=service_data[4])
        tick_box(element='hotelRestaurant.exceptionalView', value=service_data[5])
        tick_box(element='hotelRestaurant.themeRestaurant', value=service_data[6])
        tick_box(element='hotelRestaurant.mealSwim', value=service_data[7])
        tick_box(element='hotelRestaurant.petsAllowed', value=service_data[8])
        tick_box(element='hotelRestaurant.terrasse', value=service_data[9])

        
        # Tickbox Classifications & labels
        class_data = restaurants[f'{keys}'][7]['Classifications']
        tick_box(element='hotelRestaurant.michelin1', value=class_data[0])
        tick_box(element='hotelRestaurant.michelinBibGourmand', value=class_data[1])        
        tick_box(element='hotelRestaurant.michelin2', value=class_data[2])
        tick_box(element='hotelRestaurant.aAA', value=class_data[3])
        tick_box(element='hotelRestaurant.michelin3', value=class_data[4])
        
        # Menus
        menus_data = restaurants[f'{keys}'][8]['Menus']
        tick_box(element='hotelRestaurant.childMenu', value=menus_data[0])
        tick_box(element='hotelRestaurant.saltFreeMenu', value=menus_data[1])
        tick_box(element='hotelRestaurant.delightMenu', value=menus_data[2])
        tick_box(element='hotelRestaurant.vegetarianMenu', value=menus_data[3])
        tick_box(element='hotelRestaurant.halalMenu', value=menus_data[4])
        tick_box(element='hotelRestaurant.brunchMenu', value=menus_data[5])
        tick_box(element='hotelRestaurant.glutenFreeMenu', value=menus_data[6])
        tick_box(element='hotelRestaurant.kosherMenu', value=menus_data[7])
            
        # Find Update Button
        driver.execute_script('submitFormRestaurant();')
        time.sleep(1)
        
        # get response
        get_response(driver=driver, code='RT', error=error)
        
    # print result to user    
    print(f'All restaurants has been loaded to {hotel_rid}!')
    print("don't forget to add description!")
    if len(error) != 0:
        for i in error:
            print(i)
    
