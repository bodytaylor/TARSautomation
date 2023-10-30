import pandas as pd
from functions import *
import re
from hod_function import *

# get room code and store as list
def get_room_data():
    excel_file_path = f'hotel_workbook\A545\A545.xlsm'
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

# hotel_rid = input('Enter Hotel RID: ')  

# read excel file
df = get_room_data()


# start looping!
for index, row in df.iterrows():
    # add bedding type
  for i, item in enumerate(row['bedtype']):

    bed_num = item[0]
    bed_type = item[1]
    bed_index = find_text_index(text=bed_type, list=bed_type_list)
    print(bed_index)

    
    
  print(f"Added to HOD: {row['room_code']}")
        
        
