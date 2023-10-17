import pyautogui
from functions import *
import pandas as pd
from dictionary import *

# Function to count even rows until an empty cell is encountered
def count_rows(sheet, column_letter, start_row):
    row_count = 0
    row = start_row
    
    while True:
        cell_value = sheet[column_letter + str(row)].value
        if cell_value is None:
            break
        if cell_value is not None:
            row_count += 1
        row += 3
    
    return row_count

# find type of product
def find_type(df, code):
    code = str(code).strip()
    if code in df['code'].values:
        result = df.loc[df['code'] == code].values[0].astype(str).tolist()
        return result[2]
    else:
        return None

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Load product library
csv_path = 'products_lib.csv'
product_lib_df = pd.read_csv(
    csv_path,
    header=0,
    sep=';'
)

# Load workbook and read the data
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Bar"  
bars = {}
try:
    # Load Excel file and select the sheet
    workbook, sheet = load_excel_file(excel_file_path, sheet_name)
    
    if workbook and sheet:
        # Count even rows
        row_count = count_rows(sheet, "B", 14)
        print(f"Content book contain: {row_count} item(s)")

        # Loop through the rows and enter data
        cell_start = 14
        for i in range(row_count):
            # Get data from excel file
            bar_code = str(sheet[f"D{cell_start}"].value).split()
            bar_code = str(bar_code[0])
            # bar name
            bar_name = sheet[f"B{cell_start}"].value
            description = sheet[f"E{cell_start + 1}"].value
            
            # create dict
            bars[bar_name] = [
                {'Code': bar_code},
                {'Description': description}
            ] 
            
            cell_start += 3

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the workbook
    if workbook:
        workbook.close() 


# Start Looping!
for keys in bars:
    # find type
    
    bar_code = bars[f'{keys}'][0]['Code']
    code_type = bar_dic[bar_code]
    description = bars[f'{keys}'][1]['Description']
    keys = keys.upper()
    
    # Open webbrowser
    url = f'https://dataweb.accor.net/dotw-trans/translateHotelBar!input.action?actionType=translate&hotelBar.barType.code={code_type}&hotelBar.name={keys}&'
    open_web(url)
    find_logo()
    
    # Click on translation button
    find_and_click_on('img\\translate.png')
    time.sleep(2)
    
    # Click on menu and locate Translate a restaurant input box
    find_and_click_on(r'img\translate_bar.PNG')
    time.sleep(1)
    tabing(6)
    
    type_translate(2, description)
    
    # Translate and close the page
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')
    
    
print(f'All Bar(s) has been loaded to {hotel_rid}!')
print("don't forget to add description!")
