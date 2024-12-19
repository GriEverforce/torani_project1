import PyPDF2
import re
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
from app_logger import logger
import constants


# Use regular expressions to find the key-string and the value next to it

# This script uses [\S]+ to match any sequence of non-whitespace characters, which should help 
# in capturing full values like '10/14/2024' and '76.65'.

# The text is split into lines using split('\n').
# If the value is not found on the same line as the key-string, the script checks the next line starting at the same position.

# def extract_value_from_pdf(pdf_file_path, key_string):
#     with open(pdf_file_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text += page.extract_text()

#     # Use regular expressions to find the key and the value next to it
#     pattern = re.compile(rf'{key_string}\s+([\S]+)')
#     match = pattern.search(text)
#     if match:
#         return match.group(1)
#     else:
#         return None

# # Example usage
# pdf_file_path = 'po_sample.pdf'
# key_string = 'PO DATE'  # or 'TOTAL AMOUNT'
# key_string = 'TOTAL AMOUNT'
# key_string = 'SHIP TO ADDRESS CONT’D'
# value = extract_value_from_pdf(pdf_file_path, key_string)
# if value:
#     print(f'The value for "{key_string}" is "{value}"')
# else:
#     print(f'Key "{key_string}" not found in the PDF')

import PyPDF2
import re


def remove_symbols(input_string, symbols_to_be_removed):
    # Create a translation table that maps each symbol to None
    translation_table = str.maketrans('', '', ''.join(symbols_to_be_removed))
    
    # Use the translate method to remove the symbols
    return input_string.translate(translation_table)

# # Example usage:
# input_string = "Hello-World:This#is:an-example"
# symbols_to_remove = ['-', ':', '#']
# cleaned_string = remove_symbols(input_string, symbols_to_remove)
# print(cleaned_string)


# Before checking if the key sting is present, we will do the following
# 1. Remove the following from the lines of the PDF document
#   a) whitespaces 
#   b) symbols: '-', ':', '#'.
# Example:  It could be 'PO Number' or 'PO Number:'

# def extract_value_from_pdf(pdf_file_path, key_string_list):
#     logger.info(f"key_string_list: {key_string_list}")
#     with open(pdf_file_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text += page.extract_text()

#     for key_string in key_string_list:
#         lines = text.split('\n')
#         for i, raw_line in enumerate(lines):
#                 # logger.info(f"key_string_list:'{key_string_list}' raw_line: '{raw_line}'")
#                 line = "".join(raw_line.split()) # Remove whitespaces
#                 line = remove_symbols(line, constants.symbols_to_remove)
#                 line = line.upper()
#                 key_string = "".join(key_string.split()) # Remove whitespaces
#                 key_string = key_string.upper()
#                 logger.info(f"key_string:'{key_string}' line: '{line}'")
#                 if key_string in line:
#                     # Search for the value on the same line
#                     pattern = re.compile(rf'{key_string}\s+([\S]+)')
#                     match = pattern.search(line)
#                     if match:
#                         logger.info(f"key_string '{key_string}' found match:{match}")
#                         return match.group(1)
#                     # If not found, check the next line
#                     if i + 1 < len(lines):
#                         next_line = lines[i + 1]
#                         next_line_pattern = re.compile(r'(\S+)')
#                         next_line_match = next_line_pattern.match(next_line)
#                         if next_line_match:
#                             return next_line_match.group(1)
#         return None


# working
def extract_value_from_pdf(pdf_file_path, raw_key_string):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    lines = text.split('\n')
    for i, raw_line in enumerate(lines):
        # logger.info(f"raw_key_string:'{raw_key_string}' raw_line: '{raw_line}'")
        line = "".join(raw_line.split())
        line = line.upper()
        key_string = "".join(raw_key_string.split())
        key_string = key_string.upper()
        logger.info(f"key_string:'{key_string}' line: '{line}'")
        if key_string in line:
            # Search for the value on the same line
            pattern = re.compile(rf'{key_string}\s+([\S]+)')
            match = pattern.search(line)
            if match:
                return match.group(1)
            # If not found, check the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_line_pattern = re.compile(r'(\S+)')
                next_line_match = next_line_pattern.match(next_line)
                if next_line_match:
                    return next_line_match.group(1)
    return None




# # Example usage
# pdf_file_path = 'email_body_po.pdf'
# # pdf_file_path = 'repository_cfd/po-dir/po_sample2.pdf'
# key_string = 'PO DATE'  # or 'TOTAL AMOUNT'
# key_string = 'TOTAL AMOUNT'
# key_string = 'ORDER NUMBER:(For Pick-up Reference Only'
# key_string = 'SHIP DATE:'
# key_string = 'PO Date'
# value = extract_value_from_pdf(pdf_file_path, key_string)
# if value:
#     print(f'The value for "{key_string}" is "{value}"')
# else:
#     print(f'Key "{key_string}" not found in the PDF')
