from spellchecker import SpellChecker
import re
from contentbook import *

def visualize_errors(text, errors):
    # Add markers around detected errors for visualization
    for error in errors:
        text = re.sub(re.escape(error), f'**{error}**', text)

    return text
    
def detect_misspelling_and_punctuation(text):
    # Initialize spellchecker
    spell = SpellChecker()

    # Split the text into words
    words = re.findall(r'\b\w+\b', text)

    # Check for misspelled words
    misspelled_words = spell.unknown(words)
        
    # Check for punctuation
    punctuation_errors = re.findall(r'\b\w* ?[^\w\s]\w*\b', text)
    double_spaces = re.findall(r'\s{2,}', text)
    # Combine misspelled words and punctuation errors
    errors = list(misspelled_words) + punctuation_errors + double_spaces
    visualized_text = visualize_errors(text, errors)
    
    return visualized_text
    
def description_spell_check(df, col, new_colname='spell_check_result'):
    df[new_colname] = df.apply(lambda x: detect_misspelling_and_punctuation(text=x[col]), axis=1)
    print(df)
    return df

hotel_content = ContentBook(r'hotel_workbook\B4W2\B4W2.xlsm')

excel_file_path = 'output.xlsx'
description_spell_check(df=hotel_content.room_description_df, col='tar_ref').to_excel(excel_file_path, index=False)

