import TarsAutomation as ta
import openpyxl

# get multiple excel value and store it as list
def get_excel_values(file_path=str, sheet_name=str, cell_addresses=list):
    try:
        # Open the Excel file
        workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)

        # Select the specific sheet
        sheet = workbook[sheet_name]
        cell_values =[]
        for cell in cell_addresses:
            cell_values.append(sheet[cell].value)
        return cell_values
         
    except Exception as e:
        print(f"An error occurred while loading the Excel file: {str(e)}")
        return None, None
    finally:
        # Close the workbook
        if workbook:
            workbook.close()

def add(hotel_rid, hotel_content):

    # mandatory meal option *** Add According to Pricing book Need to Update
    meal_options_list = []
    
    meal_data = get_excel_values(file_path=f'hotel_workbook\{hotel_rid}\{hotel_rid} Pricing Book Hotel Creation v1.7.xlsx',
                                 sheet_name='Set-up table',
                                 cell_addresses=['E459',
                                                 'E460',
                                                 'E461',
                                                 'E462',
                                                 'E465',
                                                 'E466',
                                                 'E467',
                                                 'E468',
                                                 'E475']
                                 )
    
    # Append to meal option list
    mbreak = meal_data[0]
    mphb = meal_data[1]
    mpfb = meal_data[2]
    packai = meal_data[3]
    dmbrea = meal_data[4]
    dmphb = meal_data[5]
    dmpfb = meal_data[6]
    dpacka = meal_data[7]
    mbuff = meal_data[8]
    
    if mbreak is not None:
        meal_options_list.extend(['MBREAK', 'AMBREA'])
    if mphb is not None:
        meal_options_list.extend(['MPHB', 'AMPHB'])
    if mpfb is not None:
        meal_options_list.extend(['MPFB', 'AMPFB'])
    if packai is not None:
        meal_options_list.extend(['PACKAI', 'APACKA'])
    if dmbrea is not None:
        meal_options_list.append('DMBREA')
    if dmphb is not None:
        meal_options_list.append('DMPHB')
    if dmpfb is not None:
        meal_options_list.append('DMPFB')
    if dpacka is not None:
        meal_options_list.append('DPACKA')
    if mbuff is not None:
        meal_options_list.append('MBUFF')  
        
    # Print Data to user
    ta.logger.info(f'Meal Plan to add to the Hotel: {meal_options_list}')

    ta.get('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
    ta.wait_for_element(element='classicTabName')
    
    # start Loop!
    for item in meal_options_list:
        add = (ta.add_product(item, df=hotel_content.product_lib_df))
        ta.driver.execute_script(add)
        # Wait for page to load
        ta.wait_for_element(element='formTitle')
        
        # Meal is paying product
        ta.tick_box(element='hotelProduct.paying')
        ta.input_text(element_id='hotelProduct.maxOccupancyTotal', text='1')
        ta.input_text(element_id='hotelProduct.maxQtyInRoom', text='1')
        ta.input_text(element_id='hotelProduct.orderInResaScreen', text='99')
        ta.input_text(element_id='hotelProduct.maxOccupancyAdult', text='1')
        ta.tick_box(element='hotelProduct.availableOnGDSMedia')
        ta.click_button(element='hotelProduct.submitButton')
        
        # Wait for response
        ta.get_response(hotel_rid, code=item)
        
    ta.logger.info(f'{hotel_rid} : Mandatory Meal Option has been added')

        