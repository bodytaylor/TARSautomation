import TarsAutomation as ta

def add(hotel_rid, hotel_content):
    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    ta.wait_for_element(element='classicTabName')
    df = hotel_content.sport_leisure_df
    code_not_found = []
    
    for index, row in df.iterrows():
        code = row['product_code']
        on_site = row['on_site']
        paying = row['paying']
        product_to_add = ta.add_product(code, df=hotel_content.product_lib_df)
        if product_to_add == None:
            ta.logger.error(f'{hotel_rid} : {code} Product not found in Product Library')
            code_not_found.append(code)
        else:
            # Click Add
            ta.driver.execute_script(product_to_add)
            # Wait for page to load
            ta.wait_for_element(element='formTitle')
            
            # is product onsite or close by?
            if on_site == 'No':
                ta.driver.execute_script('document.getElementById("hotelProduct.onSiteCloseBy0").checked = true;')
                    
            # check if it paying ?
            if paying == 'Yes':
                ta.tick_box(element='hotelProduct.paying')
                ta.input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
                ta.input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
                ta.input_text(element_id='hotelProduct.orderInResaScreen', text='99')
                ta.input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')

            # always tick on available on GDS
            ta.tick_box(element='hotelProduct.availableOnGDSMedia')
            
            # Click Add
            ta.click_button(element='hotelProduct.submitButton')
            
            # Wait for response
            ta.get_response(hotel_rid, code)
                            
    if len(code_not_found) != 0:
        ta.logger.warning(f'Please Manually Check this product: {code_not_found}')

            