def keep_lines_with_text(input_file, output_file, text_to_keep):
    try:
        with open(input_file, 'r') as input_file:
            with open(output_file, 'w') as output_file:
                for line in input_file:
                    if text_to_keep in line:
                        output_file.write(line)

        print(f"Lines not containing '{text_to_keep}' have been removed.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "code\input.text"  # Replace with the path to your input file
    output_file = "output.txt"  # Replace with the path to your output file
    text_to_keep = "addBasicElement"  # Replace with the text you want to keep in the lines

    keep_lines_with_text(input_file, output_file, text_to_keep)
