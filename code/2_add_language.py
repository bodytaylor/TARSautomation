import time
import pyautogui
import webbrowser
import pandas as pd
from functions import *

# user input for Hotel RID
hotel_rid = input('Enter Hotel RID: ')

# Get Contry and city infomation from content book
excel_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
country_and_city = get_excel_values(file_path=excel_file, cell_addresses=['J41', 'C39'], sheet_name='Address&Setup')

# read excel ref file
file_path = r'R_Reference for hotel creation.xlsx'
df = pd.read_excel(file_path, 
                   sheet_name='Language per destination', 
                   usecols='A:T',
                   skiprows=4 
                   )

# filter df
while True:
    df_filtered = df[(df['COUNTRY NAME'] == country_and_city[0]) & (df['CITY NAME'] == country_and_city[1])]
    print(df_filtered)
    if len(df_filtered) == 0:
        country_and_city[1] = str(input('Please input the closest major city: '))
    elif len(df_filtered) != 0:
        break

# Drop NaN
df_filtered = df_filtered.dropna(axis=1)
total_lang = df_filtered.shape[1]

# filter ref language
mask = df_filtered.eq('ref')
ref_lang = mask.any().idxmax()

# drop default language before loading
col_drop = ['CITY NAME', 'COUNTRY NAME', 'FR', str(ref_lang)]
df_filtered.drop(columns=col_drop, inplace=True)

# create list from col head
lang_to_add = df_filtered.columns.to_list()

# fuction for adding language
def add_language(lang):
    text = f"window.confirm = ajaxReplace('dataForm', 'addHotelLanguage.action?language.languageCode={lang}', 'get');"
    type_and_enter(text)
    time.sleep(1)

# open language definition page
find_edge_console()
go_to_url("https://dataweb.accor.net/dotw-trans/secure/hotelLanguagesInput.action")
time.sleep(2)

# start loop
for item in lang_to_add:
    add_language(lang=item)

print(f'Task complete total language is {total_lang - 2}')
print(f"Don't forget to Manually set Reference language to {ref_lang}")
