import csv
import pandas as pd
import sys

# user input for Hotel RID
hotel_rid = str(input('Enter Hotel RID: '))
# Make it All Cap
hotel_rid = hotel_rid.upper()

# get room type information
# Gathering nessesory information from content book Brand, Country, PMS, GPS not send
excel_file_path = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
sheet_name = "Roomtypes"

df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

selected_columns = ['Unnamed: 2']
df = df.dropna(subset=selected_columns)
df = df.dropna(axis=1)
df = df.drop([7,8])
df = df.reset_index(drop=True)
pd.set_option('display.max_columns', None)
keep =['Unnamed: 2', 'Unnamed: 26', 'Unnamed: 19']
df = df[keep]
df = df.rename(columns={
    'Unnamed: 2': 'code',
    'Unnamed: 26': 'label',
    'Unnamed: 19': 'max_occ'
})


df = df.dropna()
print(df)

# Ask user for the desired code for each room type
external_code = []

# Iterate through the DataFrame and ask for user input for each row
for index, row in df.iterrows():
    while True:
        print(f"\n{row['code']}: {row['label']}")
        input_code = str(input(f"Enter a value for {row['code']}: ")).upper()

        if input_code not in external_code:
            external_code.append(input_code)
            break
        else:
            print(f"{input_code} is already in use. Please enter a unique value.")

# Add the new column to the DataFrame
df['external_code'] = external_code

# Display the updated DataFrame
print(df)

# Ask the user for confirmation
user_input = input("Are you sure you want to continue? (y/n): ")

# Check the user's response
if user_input.lower() == "y":
    print("Continuing...")
elif user_input.lower() == "n":
    print("Cancelled.")
    sys.exit()
else:
    print("Invalid response. Please enter 'y' or 'n'.")

# External system code
external_system = ['1A', 'AA', 'UA', 'TW', 'WB', 'DQ', 'HO', 'TE']
use_tar_code = ['DQ', 'HO', 'TE']

# Action: A
# HRID: Ask User
# Tars Key: blank
# Rate Level: blank
# Product -> from content book 	
# External System Code:	1A, AA, UA, TW, WB, DQ, HO, TE
# External Code: if 1A, AA, UA, TW, WB, -> external code ask user if DQ, HO, TE -> USE TARS CODE
# Nb Pax    -> Create one line per number of pax in that room e.g. max occ 2 create two line with value 1 and 2
# Tars Key Type -> leave blank
# Declared in Systems -> No	
# Booking Limit -> No

rows = []
for index, row in df.iterrows():
    for item in external_system:
        if item in use_tar_code:
            product = row['code']
        else:
            product = row['external_code']
        for i in range(1, row['max_occ'] + 1):
            r = {
                'Action': 'A',
                'HRID': str(f'H{hotel_rid}').strip(),
                'Tars Key': '',
                'Rate Level': '',
                'Product': str(row['code']).strip(),
                'External System Code': str(item).strip(),
                'External Code': str(product).strip(),
                'Nb Pax': i,
                'Tars Key Type': '',
                'Declared in Systems': 'No',
                'Booking Limit': 'No'
            }
            rows.append(r)  
# Write to csv file inside hotel folder
csv_path = f'hotel_workbook\{hotel_rid}\H{hotel_rid}_Product_External_Mapping.csv'

with open(csv_path, 'w', newline='') as csvfile:
    header = ['Action',	'HRID',	'Tars Key',	'Rate Level', 'Product', 'External System Code', 'External Code',
              'Nb Pax',	'Tars Key Type', 'Declared in Systems',	'Booking Limit'
              ]
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
    
# End of the program
print(f'H{hotel_rid}_Product_in_External_system.csv has been created!')
print('Please upload it in Hotel Distribution -> Automate Upload\n-> External Mapping')