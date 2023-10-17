import pandas as pd
from functions import *

# Do not add this code
meal_options_list = ['MBREAK', 'MBUFF', 'DMBREA', 'AMBREA']

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Search for product lib
def add_product(code, df):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        element = f"addBasicElement('{result[0]}','{result[1]}','{result[2]}','{result[3]}','{result[4]}','{result[5]}');"
        return element
    else:
        return None

# Read Excel file and put in data frame
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = 'Main services'
row_start = 11
row_end = 37
cell_add1 = []
cell_add2 = []
cell_add3 = []
for i in range(row_start, row_end + 1):
    cell_add1.append(f'C{i}')
    cell_add2.append(f'J{i}')
    cell_add3.append(f'K{i}')
code = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add1)
available = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add2)
amount = get_excel_values(excel_file_path, sheet_name, cell_addresses=cell_add3)
df = pd.DataFrame({'code': code, 'available': available, 'amount': amount})

# clean df and filter for available product
df.dropna(subset=['available'], inplace=True)
df = df.loc[df['available'] == 'Yes']

# Load product library
csv_path = 'products_lib.csv'
product_lib_df = pd.read_csv(
    csv_path,
    header=0,
    sep=';'
)

# open web
find_edge_console()
go_to_url('https://dataweb.accor.net/dotw-trans/productTabs!input.action')
time.sleep(2)


for index, row in df.iterrows():
    code = row['code']
    if code not in meal_options_list:
        product_to_add = add_product(code, df=product_lib_df)
        type_and_enter(product_to_add)
        time.sleep(1)

        amount = row['amount']
        if pd.isna(amount) == False:
            amount = str(int(row['amount']))
            input_textf(element_id='hotelProduct.quantity', text=amount)
        
        # always yes on GDS
        tick_box(element='hotelProduct.availableOnGDSMedia')
        
        # Click add
        type_and_enter('document.getElementById("hotelProduct.submitButton").click();')
        print(f'INFO - {code} has been added')
        time.sleep(1.5)  
    
print(f'Main Product has been added to {hotel_rid}!')
