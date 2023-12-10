import csv

def compare_and_filter(original_file, new_file, output_file):
    # Read the original CSV file and store its lines in a set
    with open(original_file, 'r', newline='') as original_csv:
        original_reader = csv.reader(original_csv)
        original_lines = set(tuple(row) for row in original_reader)

    # Read the new CSV file and filter out lines already present in the original file
    with open(new_file, 'r', newline='') as new_csv:
        new_reader = csv.reader(new_csv)
        filtered_lines = [row for row in new_reader if tuple(row) in original_lines]

    # Write the filtered lines to the output file
    with open(output_file, 'w', newline='') as output_csv:
        output_writer = csv.writer(output_csv)
        output_writer.writerows(filtered_lines)

if __name__ == "__main__":
    # Provide the paths to the original, new, and output CSV files
    original_file_path = input("Please input original file path: ").replace('"', '')
    new_file_path = input("Please input new file path: ").replace('"', '')
    output_file_path = input("Please input output file path: ").replace('"', '')
    output_file_path = f'{output_file_path}\output.csv'
    # Call the function to compare and filter the files
    compare_and_filter(original_file_path, new_file_path, output_file_path)

    print("Comparison and filtering completed. Check the 'output.csv' file.")
