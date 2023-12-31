from functions import *
from datetime import date
import csv

# Discount 
def discount_cal(discount, data):
    if data is not None:
        return data * discount / 100
    else:
        return None

# Get meal plan price and write it to dictionary

rac_dict = {
    'MBREAK': '',
    'MBUFF': '',
    'MPHB': '', 
    'MPFB': '', 
    'PACKAI': '', 
    'DMBREA': '', 
    'DMPHB': '', 
    'DMPFB': '', 
    'DPACKA': '', 
    }

rlgen_dict = {
    'MBREAK': '',
    'MBUFF': '',
    'MPHB': '', 
    'MPFB': '', 
    'PACKAI': '', 
    'DMBREA': '', 
    'DMPHB': '', 
    'DMPFB': '', 
    'DPACKA': '', 
    'AMBREA': '',
    'AMPHB': '',
    'AMPFB': '',
    'APACKA': ''
    }

# Make it read from internal pricing book instead

sheet_name = input('Please enter sheetname: ')
discount_rate = input('Please Enter Discount rate: ')


# get value from file
data = get_excel_values(
    file_path=file_path,
    sheet_name=sheet_name,
    cell_addresses=['B156', 'B157', 'B158', 'B159', 'B160', 'B163', 'B164', 'B165', 'B166',
                    'D156', 'D157', 'D158', 'D159', 'D160', 'D163', 'D164', 'D165', 'D166', 'B3', 'B7']
    )

# append data to dict
rac_dict['MBREAK'] = data[0]
rac_dict['MBUFF'] = data[1]
rac_dict['MPHB'] = data[2]
rac_dict['MPFB'] = data[3]
rac_dict['PACKAI'] = data[4]
rac_dict['DMBREA'] = data[5]
rac_dict['DMPHB'] = data[6]
rac_dict['DMPFB'] = data[7]
rac_dict['DPACKA'] = data[8]
rac_dict['AMBREA'] = discount_cal(discount=discount_rate, data=data[0]) 
rac_dict['AMPHB'] = discount_cal(discount=discount_rate, data=data[2]) 
rac_dict['AMPFB'] = discount_cal(discount=discount_rate, data=data[3]) 
rac_dict['APACKA'] = discount_cal(discount=discount_rate, data=data[4])

rlgen_dict['MBREAK'] = data[9]
rlgen_dict['MBUFF'] = data[10]
rlgen_dict['MPHB'] = data[11]
rlgen_dict['MPFB'] = data[12]
rlgen_dict['PACKAI'] = data[13]
rlgen_dict['DMBREA'] = data[14]
rlgen_dict['DMPHB'] = data[15]
rlgen_dict['DMPFB'] = data[16]
rlgen_dict['DPACKA'] = data[17]
rlgen_dict['AMBREA'] = discount_cal(discount=discount_rate, data=data[9]) 
rlgen_dict['AMPHB'] = discount_cal(discount=discount_rate, data=data[11]) 
rlgen_dict['AMPFB'] = discount_cal(discount=discount_rate, data=data[12]) 
rlgen_dict['APACKA'] = discount_cal(discount=discount_rate, data=data[13])

hrid = data[18]
currency_code = data[19]
today = date.today()
current_date = today.strftime("%Y%m%d")

# create upload file
csv_file = f'hotel_workbook\{hrid[1:]}\{hrid}_Meal_Plan_Pricing.csv'
header = ['Action', 'HRID',	'Product code',	'Rate Level', 'Validity from', 
          'Validity to', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri',	'Sat', 'Sun',	
          'Update type', 'Nb pax', 'Meal plan', 'Price status', 'Amount', 
          'Currency Code', 'Unit']

rows = []
for key, value in rlgen_dict.items():
    if value is not None:
        row = {
            'Action': 'A',
            'HRID': hrid,
            'Product code': key,
            'Rate Level': 'RLGENE',
            'Validity from': current_date,
            'Validity to': '31122023',
            'Mon': 'Yes',
            'Tue': 'Yes', 
            'Wed': 'Yes', 
            'Thu': 'Yes', 
            'Fri': 'Yes',	
            'Sat': 'Yes', 
            'Sun': 'Yes',
            'Update type': 'S', 
            'Nb pax': 1, 
            'Meal plan': '', 
            'Price status': 'I', 
            'Amount': value, 
            'Currency Code': currency_code, 
            'Unit': 'P' 
        }
        rows.append(row)
        
for key, value in rac_dict.items():
    if value is not None:
        row = {
            'Action': 'A',
            'HRID': hrid,
            'Product code': key,
            'Rate Level': 'RAC',
            'Validity from': current_date,
            'Validity to': '31122023',
            'Mon': 'Yes',
            'Tue': 'Yes', 
            'Wed': 'Yes', 
            'Thu': 'Yes', 
            'Fri': 'Yes',	
            'Sat': 'Yes', 
            'Sun': 'Yes',
            'Update type': 'S',
            'Nb pax': 1,
            'Meal plan': '',
            'Price status': 'N',
            'Amount': value,
            'Currency Code': currency_code,
            'Unit': 'P'
        }
        rows.append(row)

with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    # Write data
    writer.writeheader()
    writer.writerows(rows)
    
print(f"CSV file '{csv_file}' has been created.")

