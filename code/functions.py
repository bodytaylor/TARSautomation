import time
import pyautogui
import webbrowser
import openpyxl
import urllib.parse
import re
import sys

# Find web browser console
def find_console():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\chrome console.PNG", confidence=0.8)
    while image == None:
        image = pyautogui.locateOnScreen(r"img\chrome console.PNG", confidence=0.8)
        time.sleep(2)
        print('Please Open Google Chrome Browser Console By Press CTRL + SHIFT + I')
    time.sleep(1)


# for navigate
def find_logo():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\\accor_logo.PNG", confidence=0.8)
    while image == None:
        image = pyautogui.locateOnScreen(r"img\\accor_logo.PNG", confidence=0.8)
        time.sleep(1)
    time.sleep(1)

# open web browser and go to main tab
def open_web(url):
    webbrowser.open(url)
    find_logo()
    pyautogui.click(x=70, y=229)

# Function to load Excel file and select the sheet
def load_excel_file(file_path, sheet_name):
    try:
        # Open the Excel file
        workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)

        # Select the specific sheet
        sheet = workbook[sheet_name]

        return workbook, sheet

    except Exception as e:
        print(f"An error occurred while loading the Excel file: {str(e)}")
        return None, None

# Navigate to main search box for specific code with out dropdown menu
def main_search_box(text_search, n=2):
    find_logo()
    tabing(n)
    pyautogui.press('enter')
    pyautogui.click(x=148, y=342,)
    clear_search_box(5)
    pyautogui.write(text_search)
    pyautogui.press('enter')
    
# search box with 2 choices
import time
import pyautogui

def search_with_choice(text_search, choice=1):
    find_logo()
    tabing(3)
    pyautogui.press('enter')
    time.sleep(1)
    tabing(2)
    
    click_x = 59 if choice == 1 else 153
    pyautogui.click(x=click_x, y=305)
    time.sleep(1)
    
    find_searchbox()
    clear_search_box(4)
    pyautogui.write(text_search)
    pyautogui.press('enter')
    time.sleep(1)



# tab n time to navigate menu    
def tabing(n):
    for _ in range(n):
        pyautogui.press('tab')

# Search in main page to add the translation
def go_add_translation(search_text):
    find_logo()
    pyautogui.click(x=319, y=345)
    pyautogui.typewrite(search_text)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=960, y=540)
    tabing(9)
    pyautogui.press('enter')
    find_logo()
    pyautogui.click(x=76, y=356)

# UI reset
def ui_reset():
    find_logo()
    pyautogui.click(x=26, y=195)
    tabing(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.click(x=26, y=195)

# Navigate and Type translate message in the box and tab n time to go for next input box
def type_translate(n, message):
    pyautogui.typewrite(message, interval=0.01)
    time.sleep(0.5)
    tabing(n)
    
# find exit button
def find_exit():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\exit.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()

# find search box
def find_searchbox():
    find_logo
    x, y = pyautogui.locateCenterOnScreen('img\\filter.PNG', confidence=0.8)
    pyautogui.moveTo(x, y + 30, 0.1)
    pyautogui.click()

# find and click on add item
def find_add():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\add.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()

    
# Function to enter data into a web page This function will skip None Value and leave the cell blank
def enter_data(data):
    # Loop through the data and enter it
    for value in data:
        if value != None:
            pyautogui.write(str(value))
            pyautogui.press('tab')
        else:
            pyautogui.press('tab')
        pyautogui.press('enter')

# clear a search box before enter a new search    
def clear_search_box(n):
    for _ in range(n):
        pyautogui.press('del')
        
# Extract Capital Letter
def extract_capital_letters(input_string):
    # Define the regular expression pattern to match capital letters
    pattern = r'[A-Z]'
    
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)
    
    # Convert the matches to a string
    capital_letters = ''.join(matches)
    
    return capital_letters

"""
# search products
def product_search(product_type, text_search):
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('TARSautomation\\img\\product.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    tabing(3)
    pyautogui.press('enter')

    # Search in dropdown list
    x, y = pyautogui.locateCenterOnScreen('TARSautomation\\img\\dropdown.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    pyautogui.press('(')
    time.sleep(3)
    loop_key_press(product_type)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)

        
    # Search for product code
    find_searchbox()
    clear_search_box(6)
    pyautogui.write(text_search)
    pyautogui.press('enter')
    """
    
# Action key press
def loop_key_press(text):
    split = []
    for char in text:
        split.append(char)
    for i in split:
        if i == ' ':
            pyautogui.press('space')
        else:                       
            pyautogui.press(i)
        time.sleep(0.01)

# find text or icon and click on it it will click twice
def find_and_click_on(img_path):
    x, y = pyautogui.locateCenterOnScreen(img_path , confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()
    time.sleep(1)
    pyautogui.click()
    
# find text and click 1 time
def find_and_click(img_path):
    x, y = pyautogui.locateCenterOnScreen(img_path , confidence=0.8)
    pyautogui.moveTo(x, y, 0.1) 
    pyautogui.click()
    time.sleep(1)
    
# search for non accepted charecters in data frame
def check_text(df, col, row_shift=11):
    df['Non_Matching_Chars'] = df[col].apply(find_non_matching_chars)
    accept = 0
    for index, row in df.iterrows():
        non_matching_chars = row['Non_Matching_Chars']
        if non_matching_chars:
            print(f"Row {index + row_shift} column {col}: Detected characters: '{non_matching_chars}'")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()
        
# Create a function to find non-matching characters
def find_non_matching_chars(text):
    pattern = r'[^a-zA-Z0-9*,-.: \']'
    return ''.join(re.findall(pattern, text))


# function for finding room category
def get_category_by_code(df, code):
    matching_categories = df[df['code'] == code]['category'].tolist()
    return matching_categories

# fucntion for filling tickbox
def tickbox(data=list):
    for items in data:
        if items is not None:
            pyautogui.press('space')
            tabing(1)
        else:
            tabing(1)


# search for non accepted charecters in data frame
def check_text(df, col,):
    df['Non_Matching_Chars'] = df[col].apply(find_non_matching_chars)
    accept = 0
    for index, row in df.iterrows():
        non_matching_chars = row['Non_Matching_Chars']
        if non_matching_chars:
            print(f"Row {df.iloc[index, 0]} column {col}: Detected characters: '{non_matching_chars}'")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()
            
# Check Description lengh
def check_descrip_len(df, col):
    accept = 0
    for index, description in df.iterrows():
        if len(description) > 255:
            print(f"Row {df.iloc[index, 0]} column {col}: contain more than 255 charactors")
            accept += 1
    if accept != 0:
        print('Please go back to the content book and correct it')
        sys.exit()
        
        
# Locate add product menu
def locate_product_menu():
    find_logo()
    x, y = pyautogui.locateCenterOnScreen('img\\product.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    tabing(3)
    pyautogui.press('enter')

# Search in dropdown list
def product_search(product_type):
    x, y = pyautogui.locateCenterOnScreen('img\\dropdown.PNG', confidence=0.8)
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.click()
    pyautogui.press('(')
    time.sleep(3)
    loop_key_press(product_type)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    
# Search for product code
def code_search(text_search):
    find_searchbox()
    clear_search_box(6)
    pyautogui.write(text_search)
    pyautogui.press('enter')
    
# get excel value and store it as variable
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
   
# Function for enter code in console

def type_and_enter(text):
    text = str(text)
    pyautogui.typewrite(text)
    time.sleep(0.5)
    pyautogui.press('enter')
    
# fill content -> filling the content by switch console to multiline mode
def switch_mode():
    pyautogui.hotkey('ctrl', 'shift', 'm')
    
# Browser console function
# input textbox
def input_text(element_id, text):
    if text != None:
        pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        time.sleep(0.5)
        pyautogui.press('enter')
        
def input_textf(element_id, text):
    if text != None:
        pyautogui.typewrite(f'var inputElement = document.getElementById("{element_id}"); if (inputElement)' '{ inputElement.value = 'f'"{text}";' ' }')
        pyautogui.press('enter')
    
# select dropdown
def select_dropdown(element_id, value):
    if value != None:
        pyautogui.typewrite(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        time.sleep(0.25)
        pyautogui.press('enter')

# fast track
def select_dropdownf(element_id, value):
    if value != None:
        pyautogui.typewrite(f'var selectElement1 = document.getElementById("{element_id}"); selectElement1.value = "{value}";')
        pyautogui.press('enter')
        
# Click button
def click_button(element):
    pyautogui.typewrite(f'document.getElementById("{element}").click();')
    time.sleep(0.25)
    pyautogui.press('enter')
    
# Purse text in to url
def url_parse(input):
    url_encoded = urllib.parse.quote_plus(input)
    return url_encoded

# Looking for Edge browser console= "SHOP";
def find_edge_console():
    time.sleep(1)
    image = pyautogui.locateOnScreen(r"img\console_logo.PNG", confidence=0.8)
    while image == None:
        image = pyautogui.locateOnScreen(r"img\console_logo.PNG", confidence=0.8)
        print('Open Edge browser console by pressing WIN + R and type\n%systemroot%\system32\f12\IEChooser.exe')
        time.sleep(5)
    time.sleep(1)
    press_ctrl_plus(key='l')
    time.sleep(2)
    
# Go to target url
def go_to_url(url):
    type_and_enter(text=f'window.location.href = "{url}";')
    time.sleep(3)
    find_logo()
    # clear console
    press_ctrl_plus(key='l')
    
# Cheating pressing button
def press_ctrl_plus(key):
    pyautogui.keyDown('ctrl')
    pyautogui.press(key)
    pyautogui.keyUp('ctrl')
    
# Tickbox in browser console
def tick_box(element):
    pyautogui.typewrite(f'var checkbox = document.getElementById("{element}"); checkbox.checked = !checkbox.checked;')
    pyautogui.press('enter')
    
# toggle Chrome console
def toggle_console():
    pyautogui.hotkey('ctrl', 'shift', 'i')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'shift', 'i')
    time.sleep(0.5)
    
# fuction for adding language
def add_language(lang):
    text = f"window.confirm = ajaxReplace('dataForm', 'addHotelLanguage.action?language.languageCode={lang}', 'get');"
    type_and_enter(text)
    time.sleep(1)