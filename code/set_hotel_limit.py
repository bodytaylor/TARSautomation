import TarsAutomation as ta

def add(hotel_rid):
    ta.get('https://dataweb.accor.net/dotw-trans/secure/hotelsLimitsTabs!input.action')
    ta.wait_for_element('general-box')
    
    # Increase Product limit
    ta.input_text('searchKeyword', text=hotel_rid)
    ta.search_hotel_litmit()
    ta.driver.execute_script(f"editHotelLimitElement('{hotel_rid}','0','200','30','10','','','','true','true')")
    ta.wait_for_element('hotelsLimitsFormJson')
    ta.input_text('hotelsLimits.nbProdHotel', text='1000')
    ta.input_text('hotelsLimits.maxExtra', text='500')
    ta.input_text('hotelsLimits.maxRooms', text='50')
    ta.driver.execute_script("submitHotelLimit('setHotelsLimits.action?',false);")
    ta.get_response(hotel_rid, code='Hotel Product limit Set')
    
    # Increase Rate Level Limit
    ta.check_option('rateLimit')
    ta.search_hotel_litmit()
    ta.driver.execute_script("searchHotelsLimits();")
    ta.driver.execute_script(f"editHotelLimitElement('{hotel_rid}','1','','','','100','','','true','true')")
    ta.wait_for_element('hotelsLimitsFormJson')
    ta.input_text('hotelsLimits.nbRateHotel', text='1000')
    ta.driver.execute_script("submitHotelLimit('setHotelsLimits.action?',false);")
    ta.get_response(hotel_rid, code='Hotel Rate Level Limit Set')
    
    # Increase Indexed Rates Limit 
    ta.check_option('indexRateLimit')
    ta.search_hotel_litmit()
    ta.driver.execute_script(f"editHotelLimitElement('{hotel_rid}','2','','','','','50','','true','true')")
    ta.wait_for_element('hotelsLimitsFormJson')
    ta.input_text('hotelsLimits.nbRateIndex', text='1000')
    ta.driver.execute_script("submitHotelLimit('setHotelsLimits.action?',false);")
    ta.get_response(hotel_rid, code='Hotel Indexed Rates Limit Set')
    
    # Increase Reference Rate Limit 
    ta.check_option('referenceRateLimit')
    ta.search_hotel_litmit()
    ta.driver.execute_script(f"editHotelLimitElement('{hotel_rid}','3','','','','','','10','true','true')")
    ta.wait_for_element('hotelsLimitsFormJson')
    ta.input_text(element_id='hotelsLimits.maxRateRef', text='100')
    ta.driver.execute_script("submitHotelLimit('setHotelsLimits.action?',false);")
    ta.get_response(hotel_rid, code='Hotel Indexed Rates Limit Set')
    
    