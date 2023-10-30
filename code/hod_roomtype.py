import pandas as pd
from functions import *
import re
from hod_function import *

# get room code and store as list
def get_room_data():
    excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    sheet_name = "Roomtypes"
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols='C, E, F, G, K, AC, AA', skiprows=9, nrows=15)
    df.columns = ['room_code', 'classification','standing_type', 'view', 'resa_oder', 'marketing_label', 'tar_ref']
    df = df.dropna()
    df['bedtype'] = df['marketing_label'].apply(extract_bed_type)
    df = df.sort_values(by='resa_oder', ascending=True)
    return df

# Extract bed info from marketing lebel
def extract_bed_type(text):
    pattern = r'(\d+)\s(?:super\s)?(\w{4})'
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        bed_info = [(match[0], match[1]) for match in matches]
        return bed_info
    else:
        return None

# find text in list
def find_text_index(text, list):
    for index, item in enumerate(list):
        if text.lower() in item.lower():
            return index
    return None
     
# menu list       
bed_type_list = ['', 'Bunk bed(s)', 'Double bed(s)', 'Futon(s)', 
                 'King size bed(s)', 'Queen size bed(s)', 
                 'Single bed(s)', 'Single sofa bed(s)', 
                 'Double sofa bed(s)', 'Tatami mat(s)', 
                 'Twin bed(s)', 'Water bed(s)', 
                 'Joinable bed(s)', 'Desk and bed set(s)', 
                 'Queen size sofa bed(s)']

view_list = ['Airport view', 'On Beach', 'Bay view', 'City View', 
             'Courtyard View', 'Forest view', 'Garden View', 'Golf view', 
             'Harbour view', 'Lagoon view', 'Lake View', 'Mountain view', 
             'Panorama view', 'Pool side', 'Patio', 'Park view', 'River side', 
             'Historic side view', 'Ocean/Sea view', 'Dune view', 'Sea side', 
             'Hills view']

standing_list =  ['', 'Standard', 'Classic', 'Superior', 'Deluxe', 
                  'Comfort', 'Executive', 'Junior', 'Royal', 
                  'Presidential', 'Privilege', 'Harmony', 'Family', 
                  'Opera', 'Prestige', 'MyRoom', 'Luxury', 'Business ', 
                  'Premier']

room_class_list = ['', 'Apartment', 'Suite', 'Bungalow', 'Room', 
              'Studio', 'Villa', 'Single Bed', 'Penthouse', 
              'Tent', 'Boathouses', 'Treehouse Cottage']

hotel_rid = input('Enter Hotel RID: ')  
hotel_url = input('Enter HOD Hotel Room page : ')  

# read excel file
df = get_room_data()

# find console
find_console()

# start looping!
for index, row in df.iterrows():
  # go to target url
  type_and_enter(text = f'window.location.href = "{hotel_url}";')
  time.sleep(5)
  toggle_console()
    
  # open menu
  type_and_enter(text = """
var accordionHeadings = document.querySelectorAll('.accordion-heading');
if (accordionHeadings.length > 1) {
accordionHeadings[1].click();
}
                    """)
  time.sleep(1)
    
  # select roombutton based on index -> need to re oder data based on resa oder!!
  type_and_enter(text=f"""
var selectButtons = document.querySelectorAll('.button_standard.button_select');
if (selectButtons.length >= 2) {{
    var secondSelectButton = selectButtons[{index}];
    secondSelectButton.addEventListener('click', function() {{
        console.log('Second SELECT button clicked');
    }});
    secondSelectButton.click();
  }}
                    """)
  time.sleep(3)

  # navigate to general description
  type_and_enter(text="""
var accordionHeadings = document.querySelectorAll('.accordion-heading');
if (accordionHeadings.length > 1) {
  accordionHeadings[0].click();
}
                   """)
  time.sleep(1)
    
  # click edit
  type_and_enter("""
var editButton = document.querySelector('.button_standard.button_edit'); editButton.click();                   
                   """)
  time.sleep(1)
    # select STANDING TYPE type drop down
  standing_type = row['standing_type']
  stdt_index = standing_list.index(standing_type)
    
  type_and_enter(f"""
var dropdowns = document.querySelectorAll('.pho-select-menu');
var selectedIndex = 0;
if (selectedIndex >= 0 && selectedIndex < dropdowns.length) {{
  var selectedDropdown = dropdowns[selectedIndex];
  var optionElements = selectedDropdown.querySelectorAll('.pho-option');
  if (optionElements.length > 0) {{
    optionElements[{stdt_index}].click();
  }} else {{
    console.log('No options found in the selected dropdown.');
  }}
}} else {{
  console.log('Invalid dropdown index: ' + selectedIndex);
}}
                   """)
  time.sleep(1)
    # CLASSIFICATION
  room_class = row['classification']
  room_class_index = room_class_list.index(room_class)
    
  type_and_enter(f"""
var dropdowns = document.querySelectorAll('.pho-select-menu');
var selectedIndex = 1;
if (selectedIndex >= 0 && selectedIndex < dropdowns.length) {{
  var selectedDropdown = dropdowns[selectedIndex];
  var optionElements = selectedDropdown.querySelectorAll('.pho-option');
  if (optionElements.length > 0) {{
    optionElements[{room_class_index}].click();
  }} else {{
    console.log('No options found in the selected dropdown.');
  }}
}} else {{
  console.log('Invalid dropdown index: ' + selectedIndex);
}}                   
                   """)
  time.sleep(1)
    
  # Add view
  type_and_enter("""
var addButton = document.querySelector(".add-item");
if (addButton) {
  addButton.click();
}
                   """)
  time.sleep(1)
    
  view = row['view']
  view_index = view_list.index(view)
  type_and_enter(f"""
var checkboxes = document.querySelectorAll('.modalCheckbox');
if (checkboxes.length > 20) {{
  checkboxes[{view_index}].click();
}}                 
                   """)
  time.sleep(1)
    
  # Click Save
  type_and_enter("""
var updateButton = document.querySelector(".button_submit");
if (updateButton) {
  updateButton.click();
}                   
                   """)
  time.sleep(1)
    
  ## for now tick all No *** Need Update
  type_and_enter("""
var radioElements = document.querySelectorAll('input[type="radio"][ng-model="$ctrl.descriptor.values[0].booleanValue"][ng-value="false"]');
if (radioElements) {
  radioElements.forEach(function(radioElement) {
    var radioName = radioElement.getAttribute("name");
    console.log("Radio button name: " + radioName);
    radioElement.click();
  });
}                   
                   """)
  time.sleep(3)
  press_ctrl_plus(key='l')

    # add bedding type
  for i, item in enumerate(row['bedtype']):
    type_and_enter("""
var iconElement = document.querySelector(".icon-add");
if (iconElement) {
  iconElement.click();
}
                       """)
    time.sleep(1)
        
    bed_num = item[0]
    bed_type = item[1]
    bed_index = find_text_index(text=bed_type, list=bed_type_list)
    time.sleep(1)
        
    # Select Bedding type
    type_and_enter(f"""
var dropdowns = document.querySelectorAll('.pho-select-menu');
var selectedIndex = {3 + i};
if (selectedIndex >= 0 && selectedIndex < dropdowns.length) {{

  var selectedDropdown = dropdowns[selectedIndex];
  var optionElements = selectedDropdown.querySelectorAll('.pho-option');

  if (optionElements.length > 0) {{
    optionElements[{bed_index}].click();
  }} else {{
    console.log('No options found in the selected dropdown.');
  }}
}} else {{
  console.log('Invalid dropdown index: ' + selectedIndex);
}}
                       """)
    time.sleep(3)
    press_ctrl_plus(key='l')
        
    # Enter Beding type
    type_and_enter(f"""                       
var targetIndex = {i};
var inputElements = document.querySelectorAll('input[type="number"][ng-model="innerValue"]');

if (targetIndex >= 0 && targetIndex < inputElements.length) {{
  var inputElement = inputElements[targetIndex];
  var newValue = {bed_num};
  inputElement.value = newValue;
  var event = new Event('change', {{ bubbles: true }});
  inputElement.dispatchEvent(event);
}} else {{
  console.log('Input element with index ' + targetIndex + ' not found or out of range.');
}}
              
                       """)
    time.sleep(5)
    time.sleep(2)
    # Click Save
  type_and_enter("""
var saveButton = document.querySelector('button.button_standard.button_submit');
if (saveButton) {
  saveButton.click();
} else {
  console.log('Save button not found.');
}                      
                       """)

  pyautogui.hotkey('ctrl', 't')
  pyautogui.hotkey('ctrl', 'shift', 'j')
  time.sleep(2)
    
  print(f"Added to HOD: {row['room_code']}")
        
        
