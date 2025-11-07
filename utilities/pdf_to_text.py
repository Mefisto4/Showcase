"""
Simple tool for PDF -> TXT conversion. Imitates ATS (Applicant Tracking System) parser.
"""

import fitz


def convert_pdf_to_text(pdf_file: str, output_file: str, print_output: bool = False):
    """
    Converts a PDF file to a text file.

    :param pdf_file: full path to PDF file
    :param output_file: path to output TXT file
    :param print_output: should converted text be printed out in console?
    :return: None
    """
    pdf = fitz.open(pdf_file)
    with open(output_file, "wb", encoding="utf-8") as text_file:
        for page in pdf:  # iterate the document pages
            text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
            text_file.write(text)  # write text of page
            text_file.write(bytes((12,)))  # write page delimiter (form feed 0x0C)

            if print_output:
                print(text)


if __name__ == "__main__":
    INPUT_PDF_FILE = ""
    OUTPUT_TXT_FILE = "output.txt"
    CONSOLE_PRINT = False

    convert_pdf_to_text(INPUT_PDF_FILE, OUTPUT_TXT_FILE, CONSOLE_PRINT)
