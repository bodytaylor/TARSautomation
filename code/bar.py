import TarsAutomation as ta

# bar dict
bar_dict = {
    'BAR1':	'AMERICAN BAR',
    'BAR': 'BAR',
    'IBI99': 'bar',
    'IBI01': 'bar-rendez-vous',
    'BAR7':	'DISCOTHEQUE BAR',
    'BAR6': 'LOBBY BAR',
    'LOUNGE': 'LOUNGE',
    'BAR4':	'PIANO BAR',
    'BAR2':	'POOL BAR',
    'BAR3': 'POOL SIDE SNACK BAR',
    'PRIVBA': 'PRIVATE BAR',
    'PUB': 'PUB',
    'SNACBA': 'SNACK-BAR',
    'WINBAR': 'WINE BAR',
    }

def add(hotel_rid, bar_content: dict):    
    # Open web browser
    url = 'https://dataweb.accor.net/dotw-trans/barTabs!input.action'
    ta.get(url)
    
    # Wait for page to load
    ta.wait_for_element('allBarsTabLink')
    
    # Load bar content
    bars = bar_content
    
    # Start Looping!
    for keys in bars:
        bar_code = bars[f'{keys}'][0]['Code']
        bar_code_name = bar_dict.get(bar_code)
        ta.driver.execute_script(f"addBasicElement('{bar_code}','{bar_code_name}');")
        ta.wait_for_element('formTitle')
        
        # Name
        name = str(bars[f'{keys}'][1]['Name'])
        ta.input_text(element_id='hotelBar.name', text=name)

        # Opening Hours
        opening_hour = str(bars[f'{keys}'][2]['Opening hours'])
        ta.input_text(element_id='hotelBar.openingHours', text=opening_hour)
        
        # Max seats
        max_guest = (str(bars[f'{keys}'][3]['Max seats']))
        ta.input_text(element_id='hotelBar.maxSeats', text=max_guest)
        
        # Service Tickbox
        service_data = bars[f'{keys}'][4]['Services']
        ta.tick_box(element='hotelBar.petsAllowed', value=service_data[0])
        ta.tick_box(element='hotelBar.roomService', value=service_data[1])
        ta.tick_box(element='hotelBar.lightMeal', value=service_data[2])
        ta.tick_box(element='hotelBar.musicalAnimation', value=service_data[3])
        ta.tick_box(element='hotelBar.happyHour', value=service_data[4])
        
        # Open Information
        midday_data = bars[f'{keys}'][5]['Open Information']
        ta.tick_box(element='hotelBar.mondayMidday', value=midday_data[0])
        ta.tick_box(element='hotelBar.tuesdayMidday', value=midday_data[1])
        ta.tick_box(element='hotelBar.wednesdayMidday', value=midday_data[2])
        ta.tick_box(element='hotelBar.thursdayMidday', value=midday_data[3])
        ta.tick_box(element='hotelBar.fridayMidday', value=midday_data[4])
        ta.tick_box(element='hotelBar.saturdayMidday', value=midday_data[5])
        ta.tick_box(element='hotelBar.sundayMidday', value=midday_data[6])
        
        even_data = bars[f'{keys}'][5]['Open Information']
        ta.tick_box(element='hotelBar.mondayEvening', value=even_data[0])
        ta.tick_box(element='hotelBar.tuesdayEvening', value=even_data[1])
        ta.tick_box(element='hotelBar.wednesdayEvening', value=even_data[2])
        ta.tick_box(element='hotelBar.thursdayEvening', value=even_data[3])
        ta.tick_box(element='hotelBar.fridayEvening', value=even_data[4])
        ta.tick_box(element='hotelBar.saturdayEvening', value=even_data[5])
        ta.tick_box(element='hotelBar.sundayEvening', value=even_data[6])
        
        # Rank
        bar_rank = str(bars[f'{keys}'][6]['Rank'])
        ta.input_text(element_id='hotelBar.rank', text=bar_rank)
        
        # Find Update Button
        ta.driver.execute_script('submitFormBar();')
        
        # get response
        ta.get_response(hotel_rid, code=bar_code)