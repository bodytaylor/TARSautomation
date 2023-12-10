import TarsAutomation as ta

# attractions dict
surrouding_dict = {
    'ADML':	'Administrative Location',
    'AIRP':	'Airport',
    'SKI': 'At a ski lift',
    'BAR': 'Bar',
    'BAY': 'Bay',
    'BUS': 'Bus stop',
    'AFFA':	'Business & financial district',
    'CANL':	'Canal',
    'CITY':	'City center',
    'DOWN':	'City downtown',
    'NCIT':	'Closest major urban centre',
    'CENT':	'Distance from city centre',
    'NPT1':	'Domestic airport 1 - full name',
    'NAP1':	'Domestic airport 1 - IATA code',
    'NPT2':	'Domestic airport 2 - full name',
    'NAP2':	'Domestic airport 2 - IATA code',
    'NPT3':	'Domestic airport 3 - full name',
    'NAP3':	'Domestic airport 3 - IATA code',
    'THEA':	'Entertainment/theatre district',
    'FERR':	'Ferries',
    'HELI':	'Helipad/aerodrome',
    'HEXI':	'Highway exit',
    'APT1':	'Int. airport 1 - full name',
    'AER1':	'Int. airport 1 - IATA code',
    'APT2':	'Int. airport 2 - full name',
    'AER2':	'Int. airport 2 - IATA code',
    'APT3':	'Int. airport 3 - full name',
    'AER3':	'Int. airport 3 - IATA code',
    'APT4':	'Int. airport 4 - full name',
    'AER4':	'Int. airport 4 - IATA code',
    'APT5':	'Int. airport 5 - full name',
    'AER5':	'Int. airport 5 - IATA code',
    'MARI':	'Marina',
    'HARD':	'Marine terminal',
    'METR':	'Metro/underground/subway',
    'MONT':	'Mountain',
    'NAPA':	'National park',
    'PLGN':	'Nearby',
    'NCC': 'Nearest major city - code',
    'NCN': 'Nearest major city - name',
    'PLAG':	'On the beach',
    'VIEW':	'Panoramic view',
    'PARK':	'Park',
    'PCC': 'Primary city code',
    'PCN': 'Primary city name',
    'STAT':	'Railway and underground station',
    'GARE':	'Railway station',
    'RSTO':	'Restaurant',
    'RIVE':	'River',
    'SHOP':	'Shopping district',
    'THTR':	'Theatre',
    'SNCF':	'TRAIN + HOTEL GARE SNCF',
    'TRAM':	'Tramway',
    'VALL':	'Valley',
    'SVIE':	'With sea view',
    'WOOD':	'Wood/forest',
    'ADMI':	'Administrative building',
    'ENT': 'Amusement park',
    'APAR':	'Amusement park',
    'AQU': 'Aquarium',
    'ARTC':	'Art and Culture',
    'PLGA':	'Beach area',
    'BOT': 'Botanical gardens',
    'EVNT':	'Business centre',
    'CAS': 'Casino',
    'CINE':	'Cinema district',
    'CLIN':	'Clinic/hospital',
    'COLL':	'College/university',
    'COMP':	'Company',
    'CONC':	'Concert hall',
    'CONG':	'Convention centre',
    'CULT':	'Cultural centre',
    'EMBA':	'Embassy',
    'ENTE':	'Entertainment and theatre',
    'ENTC':	'Entertainment centre',
    'EVNS':	'Events centre',
    'EXHI':	'Exhibition and convention centre',
    'EXPO':	'Exhibition centre',
    'GOLF':	'Golf course',
    'HIST':	'Historic monument',
    'HOPI':	'Hospital',
    'INDU':	'Industrial area',
    'LAKE':	'Lake',
    'MALL':	'Mall and Shopping Centre',
    'MILI':	'Military base',
    'MOVI':	'Movie theatre',
    'MUSM':	'Museums',
    'TSP': 'Nearest transport',
    'OPE': 'Opera/symphony/concert hall',
    'OATT':	'Other attractions',
    'OTBU':	'Other point of business interest',
    'RELI':	'Place of worship',
    'CTR1':	'Primary point of interest',
    'RAC': 'Racetrack',
    'REST':	'Restaurant and cafe district',
    'SCHO':	'School/university',
    'SHOM':	'Shopping centre/mall',
    'PIST':	'Ski area',
    'DIVE':	'Special tourist area',
    'TOUR':	'Special tourist area',
    'CSPO':	'Sports centre',
    'SPOR':	'Sports centre',
    'STAD':	'Stadium',
    'ATOU':	'Tourist attraction',
    'INFO':	'Tourist information',
    'WORL':	'World Trade Center',
    'ZOO':	'Zoo',
    'PZOO':	'Zoological park',
    }

def add(hotel_rid, hotel_content):
    
    url = 'https://dataweb.accor.net/dotw-trans/ipTabs!input.action'
    ta.get(url)
    ta.wait_for_element('allIpsTabLink')
    
    # Get data from Content Book
    main_attractions = hotel_content.main_attractions
    unit_select = hotel_content.unit_select
    
    for code, *info in main_attractions.items():
        name, ofi, shuttle, shuttle_service_type, distance, minute_walk, minute_drive = info[0]

        # Add
        code_name = surrouding_dict.get(code)
        ta.driver.execute_script(f"addBasicElement('{code}','{code_name}');")
        ta.wait_for_element('formTitle')
        
        # Write Name
        ta.input_text(element_id='hotelIp.name', text=name)
        
        # Shuttle service
        if ((shuttle == 'Yes free') or (shuttle == 'Yes paying')): # Tick on Shuttle
            ta.driver.execute_script('var checkbox = document.getElementById("hotelIp.shuttle"); checkbox.checked = !checkbox.checked; changeShuttleValue();')
            if shuttle_service_type == 'On call':
                ta.tick_box(element='hotelIp.shuttle.onCall')

            if shuttle_service_type == 'Scheduled':
                ta.tick_box(element='hotelIp.shuttle.scheduled')
                
            if shuttle == 'Yes free':
                ta.tick_box(element='hotelIp.shuttle.free')

        # Distance 
        if distance != None:
            ta.driver.execute_script(f'var DistanceInput = document.getElementById("{unit_select}"); DistanceInput.value = "{distance}"; (document.createEventObject ? DistanceInput.fireEvent("onchange", document.createEventObject()) : DistanceInput.dispatchEvent(new Event("change")));')
        
        # Minute Walk
        if minute_walk == None:
            ta.input_text(element_id='hotelIp.walkingTime', text='99')
        else:
            ta.input_text(element_id='hotelIp.walkingTime', text=str(minute_walk))
        
        # Minite Drive
        if minute_drive == None:
            pass
        else:
            ta.input_text(element_id='hotelIp.carTime', text=str(minute_drive))
        
        # Orientation to the hotel
        if ofi != 0:
            ta.select_dropdown(element_id='hotelIp.orientation', value=str(ofi))
        
        # Always Tick on Available on GDS and Media
        ta.tick_box(element='hotelIp.availableOnGdsMedia')
        
        # Click Add
        ta.driver.execute_script('submitFormIp();')
        
        # Print the response
        ta.get_response(hotel_rid, code)
        