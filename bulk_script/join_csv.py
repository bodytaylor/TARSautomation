import os
import pandas as pd

# Prompt the user to enter the folder path
folder_path = input("Enter the folder path containing CSV files: ")

# Check if the entered path is valid
if not os.path.isdir(folder_path):
    print("Invalid folder path. Please provide a valid path.")
else:
    # Initialize an empty list to store DataFrames
    data_frames = []

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # Read each CSV file and append it to the data_frames list
            data = pd.read_csv(file_path, dtype=str)
            data_frames.append(data)

    # Concatenate all DataFrames in the list
    merged_data = pd.concat(data_frames, ignore_index=True)

    # Save the merged data to a new CSV file in the same folder
    output_path = os.path.join(folder_path, 'merged_data.csv')
    merged_data.to_csv(output_path, index=False)

    print(f"CSV files in the folder have been merged into '{output_path}'")
