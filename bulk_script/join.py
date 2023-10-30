import os
import glob

def join_text_files_in_folder(folder_path, output_file):
    try:
        with open(output_file, 'w') as output:
            # Use glob to find all text files in the specified folder
            text_files = glob.glob(os.path.join(folder_path, '*.log'))

            # Iterate through each text file and append its content to the output file
            for text_file in text_files:
                with open(text_file, 'r') as file:
                    output.write(file.read())
                    output.write('\n')  # Add a newline between file contents

        print(f"Text files in '{folder_path}' have been successfully joined into '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    folder_path = "data_test"  # Replace with the path to your folder
    output_file = "joined_output.txt"  # Replace with the desired output file name

    join_text_files_in_folder(folder_path, output_file)
