import TarsAutomation as ta

# version 1.0.2
def add(hotel_rid, hotel_content):
    # set file path and url
    products_df = hotel_content.products_df
    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    ta.wait_for_element('classicTabName')
    
    # Start Loop
    products_not_found = []
    
    for index, row in products_df.iterrows():
        code = row['Code']
        add = ta.add_product(code, df=hotel_content.product_lib_df)
        if add == None:
            products_not_found.append(code)
            ta.logger.error(f'{hotel_rid} : {code} Product not found in Product Library')
        else:
            ta.driver.execute_script(add)
            # Wait for page to load
            ta.wait_for_element('formTitle')
            
            if row['paying'] == 'Yes':
                ta.tick_box(element='hotelProduct.paying')
                ta.input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
                ta.input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
                ta.input_text(element_id='hotelProduct.orderInResaScreen', text='99')
                ta.input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')
                
            ta.tick_box(element='hotelProduct.availableOnGDSMedia')
            ta.click_button(element='hotelProduct.submitButton')
            
            # Check if response is OK
            ta.get_response(hotel_rid, code)
           
    if len(products_not_found) != 0:
        ta.logger.warning(f'Please Manually Check this product: {products_not_found}')
        
    