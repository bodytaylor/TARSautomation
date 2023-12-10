import pandas as pd
import TarsAutomation
from TarsAutomation import logger
from functions import get_excel_values

def get_lang_ref(hotel_rid):
    # Get Contry and city infomation from content book
    ref_file = f'hotel_workbook\{hotel_rid}\{hotel_rid}.xlsm'
    country_and_city = get_excel_values(file_path=ref_file, cell_addresses=['J41', 'C39'], sheet_name='Address&Setup')

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
        print(country_and_city)
        
        if len(df_filtered) == 0:
            print('No Reference Found!')
            country_and_city[1] = str(input('Please input the closest major city: ')).upper()
            
        elif len(df_filtered) != 0:
            break
        # Drop NaN
    df_filtered = df_filtered.dropna(axis=1)

    # filter ref language
    mask = df_filtered.eq('ref')
    ref_lang = mask.any().idxmax()

    # drop default language before loading
    col_drop = ['CITY NAME', 'COUNTRY NAME', 'FR', str(ref_lang)]
    df_filtered.drop(columns=col_drop, inplace=True)

    # create list from col head
    lang_to_add = df_filtered.columns.to_list()
    logger.info(f'Language to add : {lang_to_add}')
    return lang_to_add

def add(hotel_rid):
    lang_to_add = get_lang_ref(hotel_rid)
    # open language definition page
    TarsAutomation.get("https://dataweb.accor.net/dotw-trans/secure/hotelLanguagesInput.action")

    # start loop
    for language in lang_to_add:
        TarsAutomation.add_language(lang=language)
        logger.info(TarsAutomation.get_response(hotel_rid, code=language))
    
    logger.info(f'{hotel_rid} : Language Setup Done.')