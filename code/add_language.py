import pandas as pd
import TarsAutomation
from TarsAutomation import logger

def get_lang_ref(city, country):
    # read excel ref file
    file_path = r'R_Reference for hotel creation.xlsx'
    df = pd.read_excel(file_path, 
                    sheet_name='Language per destination', 
                    usecols='A:T',
                    skiprows=4 
                    )

    # filter df
    while True:
        df_filtered = df[(df['COUNTRY NAME'] == country) & (df['CITY NAME'] == city)]
        print(country, city)
        
        if len(df_filtered) == 0:
            print('No Reference Found!')
            city = str(input('Please input the closest major city: ')).upper()
            
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

def add(hotel_rid, hotel_content):
    # Get list of languages to add from reference file.
    lang_to_add = get_lang_ref(city=hotel_content.city, country=hotel_content.country)
    
    # open language definition page.
    TarsAutomation.get("https://dataweb.accor.net/dotw-trans/secure/hotelLanguagesInput.action")

    # start loop
    for language in lang_to_add:
        TarsAutomation.add_language(lang=language)
    
    logger.info(f'{hotel_rid} : Language Setup Done.')