import os
import shutil

def organize_files_by_subfolders(folder_path):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_name, file_extension = os.path.splitext(filename)
            
            # Extract the part of the file name to create the subfolder
            subfolder_name = file_name.split('_')[0]
            
            # Create the subfolder if it doesn't exist
            subfolder_path = os.path.join(folder_path, subfolder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            
            # Move the file into the subfolder
            file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(subfolder_path, filename)
            
            try:
                shutil.move(file_path, new_file_path)
                print(f"Moved '{filename}' to '{subfolder_name}' subfolder.")
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except FileExistsError:
                print(f"File '{new_file_path}' already exists in '{subfolder_name}' subfolder.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path where the files are located: ")
    organize_files_by_subfolders(folder_path)
