import TarsAutomation as ta
from functions import continue_program

def add(hotel_rid, hotel_content):
    print("[WARNING] - Please Check Loading Form and Clean up all note from the code section!")
    print("[WARNING] - V.10 DWBUS -> DWBUS1")
    print("[WARNING] - V.10 DWCCL1 -> DWCCL")
    
    continue_program()
    
    # Load Web Description Data Frame
    df = hotel_content.web_description_df

    # open web
    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    ta.wait_for_element(element='classicTabName')
    
    product_not_found = []
    # Let's rolls!
    for index, row in df.iterrows():
        code = row['Code']
        product_to_add = ta.add_product(code, df=hotel_content.product_lib_df)
        if product_to_add is None:
                ta.logger.error(f'{hotel_rid} : {code} Product not found in Product Library')
                product_not_found.append(code)
        else:
            ta.driver.execute_script(product_to_add)
            # Wait for page to load
            ta.wait_for_element(element='formTitle')
        
            # always yes on GDS
            ta.tick_box(element='hotelProduct.availableOnGDSMedia')
                
            # Click add
            ta.click_button(element='hotelProduct.submitButton')
            
            # Get response
            ta.get_response(hotel_rid, code)
            
    # Add description
    for index, row in df.iterrows():
        code = row['Code']
        if code not in product_not_found:
            type = ta.find_type(code=code, df=hotel_content.product_lib_df)
            des = row['Description']
            mk_label = row['Marketing']
            ta.product_description(code=code, description=des, marketing=mk_label, type=type, hotel_rid=hotel_rid)
            ta.translate_hotel_product()
            ta.get_response(hotel_rid, code)
            
    