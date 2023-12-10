import pandas as pd
import os

def separate_rows(input_file, column_to_separate):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Group the DataFrame by the specified column
    grouped = df.groupby(column_to_separate)

    # Get the directory of the input file
    input_dir = os.path.dirname(input_file)

    # Create a new Excel file for each group in the same folder as the input file
    for group_name, group_data in grouped:
        output_file = os.path.join(input_dir, f"{group_name}.xlsx")
        group_data.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Specify the input Excel file, column to separate, and output folder
    input_file = input(".xlsx file path: ").replace('"', "") 
    column_to_separate = input("Please input column name: ")  

    # Call the function to separate rows and write to new files
    separate_rows(input_file, column_to_separate)

    print("Separation complete.")