import TarsAutomation as ta
        
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

def add(hotel_rid, hotel_content: dict):
    restaurants = hotel_content   
    # Open web browser
    url = 'https://dataweb.accor.net/dotw-trans/restaurantTabs!input.action'
    ta.get(url)
    ta.wait_for_element(element='allRestaurantsTabLink')
    
    # Start Looping!
    for key in restaurants:
        # Find add button and start entering data
        ta.driver.execute_script("addBasicElement('RT','RESTAURANT');")
        
        # Wait for page to load
        ta.wait_for_element('hotelRestaurantFormJson')
        
        # Enter Ranking
        rank = str(restaurants[key][1]['rank'])
        ta.input_text(element_id='hotelRestaurant.rank', text=rank)
        
        # Enter name of the restaurant
        ta.input_text(element_id='hotelRestaurant.name', text=key)
        
        # Enter Opening hour
        restaurant_hours = restaurants[key][0]['open_hour']
        ta.input_text(element_id='hotelRestaurant.horaires', text=restaurant_hours)
        
        # Enter Cooking style
        cooking_style = restaurants[key][2]['cook_type']
        cooking_select = cooking_type_dict.get(cooking_style)
        ta.select_dropdown(element_id='hotelRestaurant.cookType.code', value=cooking_select)
        
        # Tickbox Open Information
        opening_data = restaurants[key][3]['Open information']
        ta.tick_box(element='hotelRestaurant.mondayMidday', value=opening_data[0])
        ta.tick_box(element='hotelRestaurant.tuesdayMidday', value=opening_data[1])
        ta.tick_box(element='hotelRestaurant.wednesdayMidday', value=opening_data[2])
        ta.tick_box(element='hotelRestaurant.thursdayMidday', value=opening_data[3])
        ta.tick_box(element='hotelRestaurant.fridayMidday', value=opening_data[4])
        ta.tick_box(element='hotelRestaurant.saturdayMidday', value=opening_data[5])
        ta.tick_box(element='hotelRestaurant.sundayMidday', value=opening_data[6])
        ta.tick_box(element='hotelRestaurant.mondayEvening', value=opening_data[7])
        ta.tick_box(element='hotelRestaurant.tuesdayEvening', value=opening_data[8])
        ta.tick_box(element='hotelRestaurant.wednesdayEvening', value=opening_data[9])
        ta.tick_box(element='hotelRestaurant.thursdayEvening', value=opening_data[10])
        ta.tick_box(element='hotelRestaurant.fridayEvening', value=opening_data[11])
        ta.tick_box(element='hotelRestaurant.saturdayEvening', value=opening_data[12])
        ta.tick_box(element='hotelRestaurant.sundayEvening', value=opening_data[13])
        
        # Tickbox Payment Information
        payment_data = restaurants[key][4]['Payment Option']
        ta.tick_box(element='hotelRestaurant.cash', value=payment_data[0])
        ta.tick_box(element='hotelRestaurant.creditCard', value=payment_data[1])
        ta.tick_box(element='hotelRestaurant.check', value=payment_data[2])
        ta.tick_box(element='hotelRestaurant.othersLocalPaymentOptions', value=payment_data[3])
        
        # Skip Ex Chef & Skip AVG price
        
        # Enter Max Seats
        max_pax = str(restaurants[key][5]['Max seats'])
        ta.input_text(element_id='hotelRestaurant.maximumSeating', text=max_pax)
        
        # Tickbox Service option
        service_data = restaurants[key][6]['Service option']
        ta.tick_box(element='hotelRestaurant.fullBoard', value=service_data[0])
        ta.tick_box(element='hotelRestaurant.halfBoard', value=service_data[1])
        ta.tick_box(element='hotelRestaurant.wheelChairAccess', value=service_data[2])
        ta.tick_box(element='hotelRestaurant.airConditionning', value=service_data[3])
        ta.tick_box(element='hotelRestaurant.nonSmoking', value=service_data[4])
        ta.tick_box(element='hotelRestaurant.exceptionalView', value=service_data[5])
        ta.tick_box(element='hotelRestaurant.themeRestaurant', value=service_data[6])
        ta.tick_box(element='hotelRestaurant.mealSwim', value=service_data[7])
        ta.tick_box(element='hotelRestaurant.petsAllowed', value=service_data[8])
        ta.tick_box(element='hotelRestaurant.terrasse', value=service_data[9])
        
        # Tickbox Classifications & labels
        class_data = restaurants[key][7]['Classifications']
        ta.tick_box(element='hotelRestaurant.michelin1', value=class_data[0])
        ta.tick_box(element='hotelRestaurant.michelinBibGourmand', value=class_data[1])        
        ta.tick_box(element='hotelRestaurant.michelin2', value=class_data[2])
        ta.tick_box(element='hotelRestaurant.aAA', value=class_data[3])
        ta.tick_box(element='hotelRestaurant.michelin3', value=class_data[4])
        
        # Menus
        menus_data = restaurants[key][8]['Menus']
        ta.tick_box(element='hotelRestaurant.childMenu', value=menus_data[0])
        ta.tick_box(element='hotelRestaurant.saltFreeMenu', value=menus_data[1])
        ta.tick_box(element='hotelRestaurant.delightMenu', value=menus_data[2])
        ta.tick_box(element='hotelRestaurant.vegetarianMenu', value=menus_data[3])
        ta.tick_box(element='hotelRestaurant.halalMenu', value=menus_data[4])
        ta.tick_box(element='hotelRestaurant.brunchMenu', value=menus_data[5])
        ta.tick_box(element='hotelRestaurant.glutenFreeMenu', value=menus_data[6])
        ta.tick_box(element='hotelRestaurant.kosherMenu', value=menus_data[7])
            
        # Find Update Button
        ta.driver.execute_script('submitFormRestaurant();')
        
        # get response
        ta.get_response(hotel_rid, code='RT')
        
    
