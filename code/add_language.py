from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from functions import *
from web_driver_init import driver

# fuction for adding language
def add_language(lang):
    script = f"window.confirm = ajaxReplace('dataForm', 'addHotelLanguage.action?language.languageCode={lang}', 'get');"
    driver.execute_script(script)
    time.sleep(1)

def add(hotel_rid):
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
        print(f'Country: {country_and_city[0]}')
        df_filtered = df[(df['COUNTRY NAME'] == country_and_city[0]) & (df['CITY NAME'] == country_and_city[1])]
        print(df_filtered)
        print(country_and_city)
        if len(df_filtered) == 0:
            country_and_city[1] = str(input('Please input the closest major city: ')).upper()
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

    # open language definition page
    driver.get("https://dataweb.accor.net/dotw-trans/secure/hotelLanguagesInput.action")
    element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h2'))
        )
    print(element.text)

    # start loop
    for item in lang_to_add:
        add_language(lang=item)

    print(f'Task complete total language is {total_lang - 2}')
    print(f"Don't forget to Manually set Reference language to {ref_lang}")
