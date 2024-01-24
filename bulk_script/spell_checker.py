import pandas as pd

def remove_char_at_index(input_str, index):
    """
    Remove character at specified index from input_str.

    Parameters:
    input_str (str): The input string.
    index (int): The index of the character to remove.

    Returns:
    str: The input string with the character at the specified index removed.
    """
    if 0 <= index < len(input_str):
        if input_str[index] == " ":
            return input_str[:index] + input_str[index+1:]
        else:
            return input_str
    else:
        return input_str

def adjust_text_length(text, max_length=47):
    """
    Adjust the length of the text
    """
    if len(text) > max_length:
        adj_text = remove_char_at_index(text, max_length)
        return adj_text
    else:
        return text

def process_excel_file(input_file, output_file, target_column):
    """
    Read an Excel file, adjust text in the specified column, and save the modified data to a new Excel file.
    """
    # Read Excel file
    df = pd.read_excel(input_file, engine='openpyxl', dtype=str)

    # Adjust text in the specified column
    df[target_column] = df[target_column].apply(adjust_text_length)

    # Save the modified data to a new Excel file
    df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    # Set the file paths and column name
    input_excel_file = r'D:\NSANGKARN\Downloads\Expedia Rollout new-19-01-2024_06-07-57 (1).xlsx'
    output_excel_file = r'D:\NSANGKARN\Downloads\Fixed_Expedia Rollout new-19-01-2024_06-07-57 (1).xlsx'
    target_column_name = 'Room Type Name'

    # Process the Excel file
    process_excel_file(input_excel_file, output_excel_file, target_column_name)

    print(f"Text adjustment completed. Modified data saved to {output_excel_file}.")
