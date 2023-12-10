import TarsAutomation as ta

def add(hotel_rid, hotel_content):
    # get room data
    room_data = hotel_content.rooms_df
    
    # open url
    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action') 
    ta.wait_for_element('classicTabName')

    try:
        for index, row in room_data.iterrows():
            # locate a menu and search for room type
            room_code = str(row['TARS product code']).strip()
            # Check Room Code
            add = (ta.add_product(code=room_code, df=hotel_content.product_lib_df))
            if add is not None:
                ta.driver.execute_script(add)
                
                # waiting for input form
                ta.wait_for_element(element='formTitle')
                
                # paying product tickbox
                ta.tick_box('hotelProduct.paying')
                    
                # book abble product tickbox
                ta.tick_box('hotelProduct.bookable')        
                        
                # Max Occupency 
                max_occ = str(row['Maximum occupancy *']).strip()
                ta.input_text(element_id='hotelProduct.maxOccupancyTotal', text=max_occ)
                        
                # Adult
                adult = str(row['Maximum adults *']).strip()
                ta.input_text(element_id='hotelProduct.maxOccupancyAdult', text=adult)
                        
                # Children
                children = str(row['Maximum children *']).strip()
                ta.input_text(element_id='hotelProduct.maxOccupancyChildren', text=children)
                        
                # Nb of beds for 1 pax
                bed_for_1 = str(row['Nb of bed available for\n1 pax *']).strip()
                ta.input_text(element_id='hotelProduct.singleBebNumber', text=bed_for_1)      
                        
                # Nb of beds for 2 pax
                bed_for_2 = str(row['Nb of bed available for\n2 pax *']).strip()
                ta.input_text(element_id='hotelProduct.doubleBebNumber', text=bed_for_2)   
                            
                # room size
                room_size = str(row['Room size m²*']).strip()
                ta.input_text(element_id='hotelProduct.roomSizeInSquareMeter', text=room_size)
                        
                # Quantity of product
                quantity = str(row['Quantity\nof product *']).strip()
                ta.input_text(element_id='hotelProduct.quantity', text=quantity)
                        
                # PMS product code -> Put room code
                ta.input_text(element_id='hotelProduct.pmsCode', text=room_code)
                        
                # Available on GDS and Media (always tick)
                ta.tick_box('hotelProduct.availableOnGDSMedia')
                        
                # Order in RESA Screen 
                order_resa = str(row['Order \nin resa \nscreen *'])
                ta.input_text(element_id='hotelProduct.orderInResaScreen', text=order_resa)
                        
                # Max quantity of the product in room -> skip
   
                # Click add
                ta.click_button(element='hotelProduct.submitButton')
                        
                # Wait for response
                ta.get_response(hotel_rid, code=room_code)
                        
            else:
                ta.logger.error(f'{hotel_rid}: {room_code} Product Not Found in Product Library.')

    except Exception as e:
        ta.logger.error(f"An error occurred: {str(e)}")
        
            