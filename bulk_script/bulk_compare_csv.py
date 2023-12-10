import os
import pandas as pd

def compare_csv_files(original_dir, new_dir):
    # Get a list of all files in the original directory
    original_files = os.listdir(original_dir)

    for file_name in original_files:
        # Construct the full file paths for the original and new files
        original_path = os.path.join(original_dir, file_name)
        new_path = os.path.join(new_dir, file_name)

        # Check if the files exist in both directories
        if os.path.exists(new_path):
            # Read CSV files into pandas DataFrames
            df1 = pd.read_csv(original_path)
            df2 = pd.read_csv(new_path)
            
            diff_rows = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)

            if not diff_rows.empty:
                print(f"Differences in file {file_name}:\n")
                print(diff_rows)
                print("\n---\n")
            else:
                print(f"The CSV files ({file_name}) are identical.")
        else:
            print(f"File ({file_name}) does not exist in the new directory.")


if __name__ == "__main__":
    # Get input for directory paths
    original_directory = input("Enter the path to the directory containing the original files: ").replace('"', '')
    new_directory = input("Enter the path to the directory containing the new files: ").replace('"', '')

    compare_csv_files(original_directory, new_directory)
