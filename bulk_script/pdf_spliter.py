import PyPDF2
import os

def split_pdf(input_path):
    # Ensure the input file exists
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    # Open the PDF file in binary mode
    with open(input_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Iterate through each page and create a new PDF for each page
        for page_num in range(len(pdf_reader.pages)):
            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()

            # Add the current page to the writer
            pdf_writer.add_page(pdf_reader.pages[page_num])

            # Create a new file name with the original file name and page number
            output_file_path = f"{os.path.splitext(input_path)[0]}_page_{page_num + 1}.pdf"

            # Write the new PDF to the output file
            with open(output_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"Page {page_num + 1} saved to {output_file_path}")

if __name__ == "__main__":
    # Get the input PDF file path from the user
    input_path = input("Enter the path of the PDF file to split: ").strip().replace('"', '')

    # Call the split_pdf function with the user-provided input path
    split_pdf(input_path)
