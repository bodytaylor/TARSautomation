import os
import pandas as pd

def xls_to_csv(xls_file, csv_file):
    try:
        # Read the XLS file into a pandas DataFrame
        df = pd.read_excel(xls_file)

        # Write the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)

        print(f"Conversion successful: {xls_file} -> {csv_file}")

    except Exception as e:
        print(f"Error converting {xls_file} to {csv_file}: {e}")

if __name__ == "__main__":
    # Replace 'input_folder' with the path to your folder containing XLS files
    
    input_folder = r'D:\NSANGKARN\Downloads\TRAVELOKA\TRAVELOKA'
    
    # Replace 'output_folder' with the path to the folder where you want to save CSV files
    output_folder = r'D:\NSANGKARN\Downloads\TRAVELOKA\TRAVELOKA\csv'

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.xls'):
            input_xls_file = os.path.join(input_folder, filename)
            output_csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
            xls_to_csv(input_xls_file, output_csv_file)
