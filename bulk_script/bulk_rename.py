import os
import re

def extract_desired_name(file_name):
    # Use a regular expression to extract a name within brackets
    match = re.search(r'\[(.*?)\]', file_name)
    
    if match:
        desired_name = match.group(1)
        return desired_name
    else:
        return None

def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            old_file_name = os.path.join(folder_path, filename)
            desired_name = extract_desired_name(filename)

            if desired_name:
                # Get the file extension
                file_extension = os.path.splitext(filename)[1]
                new_file_name = desired_name + file_extension
                new_file_path = os.path.join(folder_path, new_file_name)

                try:
                    os.rename(old_file_name, new_file_path)
                    print(f"File renamed from '{old_file_name}' to '{new_file_path}'")
                except FileNotFoundError:
                    print(f"File '{old_file_name}' not found.")
                except FileExistsError:
                    print(f"File '{new_file_path}' already exists.")
            else:
                print(f"File '{old_file_name}' does not contain the desired name in brackets.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path where the files are located: ")
    rename_files_in_folder(folder_path)
