import TarsAutomation as ta
import pandas as pd

def add(hotel_rid, hotel_content):
    df = hotel_content.main_service_df
    meal_options_list = ['MBREAK']
    product_not_found = []
    
    # open web
    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    ta.wait_for_element(element='classicTabName')
    
    for index, row in df.iterrows():
        code = row['code']
        if code not in meal_options_list:
            product_to_add = ta.add_product(code, df=hotel_content.product_lib_df)
            if product_to_add is None:
                ta.logger.error(f'{hotel_rid} : {code} Product not found in Product Library')
                product_not_found.append(code)
            else:
                ta.driver.execute_script(product_to_add)
                
                # Wait for page to load
                ta.wait_for_element(element='formTitle')

                amount = row['amount']
                if pd.isna(amount) == False:
                    amount = str(int(row['amount']))
                    ta.input_text(element_id='hotelProduct.quantity', text=amount)
                
                # always yes on GDS
                ta.tick_box(element='hotelProduct.availableOnGDSMedia')
                
                # Click add
                ta.click_button(element='hotelProduct.submitButton')
                
                # Wait for response
                ta.get_response(hotel_rid, code)
                