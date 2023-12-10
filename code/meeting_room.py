import TarsAutomation as ta

# Function to enter data into a web page
def enter_data(data):
    elements_list = ['hotelLounge.name', 'hotelLounge.surface', 'hotelLounge.maxNumberPax', 
                     'hotelLounge.ceilingHeight', 'hotelLounge.floorCover', 'hotelLounge.nbPaxBoardRoom',
                     'hotelLounge.nbPaxInU', 'hotelLounge.nbPaxClassRoom',
                     'hotelLounge.nbPaxInV', 'hotelLounge.nbPaxTheater', 'hotelLounge.nbPaxRoundTables',
                     'hotelLounge.nbPaxRoundTablesOff', 'hotelLounge.nbPaxRoundTablesDc',
                     'hotelLounge.nbPaxRoundTablesOffDc']
    
    # Loop through the data and enter it
    for i, value in enumerate(data):
        if value == None:
            ta.input_text(element_id=elements_list[i], text='0')
        else:
            ta.input_text(element_id=elements_list[i], text=str(value))

# Handle tickboxes
def meetingroom_tick_box(tickbox):
    tick_box_elements = [
        'hotelLounge.buffet', 'hotelLounge.buffetDc', 
        'hotelLounge.cocktail', 'hotelLounge.exposition'
        ]
    for i, value in enumerate(tickbox):
        if value == 'Yes':
            ta.tick_box(element=tick_box_elements[i], value=value)        

def add(hotel_rid, hotel_content):
    # Load workbook and read the data
    meeting_room = hotel_content
    
    # Open web browser and navigate to a page
    ta.get('https://dataweb.accor.net/dotw-trans/displayHotelLounges!input.action')
    ta.wait_for_element('hotelLoungesTable')
             
    for key in meeting_room:
        data = meeting_room[key][0]
        tickbox = meeting_room[key][1]
        # Add MEET
        ta.driver.execute_script("addBasicElement('MEET');")
        ta.wait_for_element('formTitle')
        
        # Enter data into the web page
        enter_data(data)
        meetingroom_tick_box(tickbox)
        
        # Click Add
        ta.driver.execute_script("if(validateForm_hotelLoungeForm($('hotelLoungeForm'))){submitLoungeForm ($('hotelLoungeForm'));}")
        
        # Print the response
        ta.get_response(hotel_rid, code=key)
            