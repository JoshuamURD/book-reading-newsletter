import PyPDF2

def extract_pdf_pages(input_file_path, output_file_path, start_page, end_page):
    """
    Extracts a range of pages from a PDF file and saves them as a new PDF file.

    Args:
        input_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        start_page (int): The first page to extract (1-indexed).
        end_page (int): The last page to extract (1-indexed).
    """
    with open(input_file_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(start_page-1, end_page):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        with open(output_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def main():
    file_path = r"C:\Users\clerk\Downloads\PLT Program Requirements.pdf"
    output_path= r"C:\Users\clerk\Downloads\test.pdf"
    start_page=2
    end_page=3
    extract_pdf_pages(file_path, output_path, start_page, end_page)


if __name__ == "__main__":
    main()