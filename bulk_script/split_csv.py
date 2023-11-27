import os
import csv

def split_csv(input_file, output_folder, lines_per_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Assuming the first row is a header

        current_line = 0
        file_count = 1
        output_file = os.path.join(output_folder, f'split_file_{file_count}.csv')

        with open(output_file, 'w', newline='', encoding='utf-8') as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(header)

            for row in reader:
                writer.writerow(row)
                current_line += 1

                if current_line >= lines_per_file:
                    current_line = 0
                    file_count += 1
                    output_file = os.path.join(output_folder, f'split_file_{file_count}.csv')
                    out_csv.close()  # Close the current file before opening the next one
                    out_csv = open(output_file, 'w', newline='', encoding='utf-8')
                    writer = csv.writer(out_csv)
                    writer.writerow(header)

if __name__ == "__main__":
    input_file_path = input('enter target file path: ')  # Change this to your input CSV file path
    output_folder_path = input('insert path for outputfile: ')  # Change this to the desired output folder path
    lines_per_file = int(input('enter lines limit per file: '))  # Change this to the desired number of lines per output file

    split_csv(input_file_path, output_folder_path, lines_per_file)
