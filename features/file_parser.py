import re
import PyPDF2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

from constants import *
from app_logger import logger  



# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Ensure newlines are preserved for splitting lines correctly
    text = text.replace('\n', ' NEWLINE ')
    return text

# Function to find key-value pairs in text, checking both same line and next line
def find_key_values(text, key_strings, value_pattern):
    val_for_key = ''
    key_value_pairs = {}
    lines = text.split(' NEWLINE ')
    for i, line in enumerate(lines):
        for key in key_strings:
            # First try to find the value on the same line
            regex = rf"(?i){key}\s*[:#-]?\s*({value_pattern})"
            match = re.search(regex, line)
            if match:
                key_value_pairs[key] = match.group(1)
                val_for_key = match.group(1)
            else:
                # If not found, check the next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    match = re.search(value_pattern, next_line)
                    if match:
                        key_value_pairs[key] = match.group(0)
                        val_for_key = match.group(0)
                    
    return key_value_pairs, val_for_key

# Main function to extract key-value pairs
# def extract_key_value_pairs(pdf_path, key_string_dict):
def extract_value_from_pdf(pdf_path, key_string, required_pattern):
    
    logger.info(f"pdf_path: {pdf_path} key_string: {key_string} required_pattern: {required_pattern}")
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # logger.info(f"pdf_text: {pdf_text}")
    # Preprocess the text to handle spaces and newlines
    preprocessed_text = preprocess_text(pdf_text)
    
    # Dictionary to hold all extracted key-value pairs
    all_key_values = {}
    
    # Iterate through the dictionary of key strings and their patterns
    # for keys, pattern in key_string_dict.items():
    # for keys, pattern in key_string_dict.items():
    #     key_value_pairs = find_key_values(preprocessed_text, keys, pattern)
    #     all_key_values.update(key_value_pairs)
    
    for keys in key_string:
        key_value_pairs, val_for_key = find_key_values(preprocessed_text, keys, required_pattern)
        all_key_values.update(key_value_pairs) # This is redundant as we are returning as soon as value is found
        if val_for_key:
            break # returning as soon as value is found
        else:
            val_for_key = ''

    logger.info(f"val_for_key: {val_for_key} keys: {keys}")
    # return all_key_values
    return val_for_key

# Define patterns for dates
# date_pattern = r'\d{1,2}-[a-zA-Z]{3}-\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{4}-\d{1,2}-\d{1,2}'

# # Sample usage
# key_string_dict = {
#     ('PO', 'PO Number', 'Purchase Order'): r'\d+',
#     ('Invoice Number', 'Invoice #', 'Invoice:', 'Inv. No.'): r'\d+',
#     ('PO Date', 'Purchase Order Date', 'PO Dt.'): date_pattern,
#     ('DATE', 'Invoice Dt.'): date_pattern
# }




# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# # Function to preprocess text
# def preprocess_text(text):
#     # Replace multiple spaces with a single space
#     text = re.sub(r'\s+', ' ', text)
#     # Replace newline characters with a space
#     text = text.replace('\n', ' ')
#     return text

# # Function to find key-value pairs in text
# def find_key_values(text, key_strings, value_pattern):
#     key_value_pairs = {}

#     for key in key_strings:
#         # Adjust regex to match key strings with optional whitespaces, case-insensitive, and consider lines with more spaces
#         regex = rf"(?i){key}\s*[:#-]?\s*({value_pattern})"
#         logger.info(f"key: '{key}' regex: {regex}")
#         if key in text:
#             logger.info(f"KEY({key}) found in TEXT:{text}")
#         matches = re.findall(regex, text)
#         if matches:
#             logger.info(f"Found key: '{key}' in text: {text}")
#             key_value_pairs[key] = matches[0]
#     return key_value_pairs


# def extract_value_from_pdf(pdf_path, key_string_list, required_pattern):

#     # Path to your PDF file
#     # pdf_path = 'repository_cfd/po-dir/email_body_po.pdf'

#     # Extract text from PDF
#     pdf_text = extract_text_from_pdf(pdf_path)

#     # Preprocess the text to handle spaces and newlines
#     preprocessed_text = preprocess_text(pdf_text)

#     key_pair = find_key_values(preprocessed_text, key_string_list, required_pattern)

#     logger.info(f"key_pair: {key_pair}")

#     key_value = 0
#     if key_pair:
#         key_list = list(key_pair.values())
#         key_value = key_list[0]
   
#     return key_value



# # if __name__ == "__main__":
# #     # Find key-value pairs
# #     po_number_values = find_key_values(preprocessed_text, po_number_key_strings, number_pattern)
# #     invoice_number_values = find_key_values(preprocessed_text, invoice_number_key_strings, number_pattern)
# #     po_date_values = find_key_values(preprocessed_text, po_date_key_strings, date_pattern)
# #     invoice_date_values = find_key_values(preprocessed_text, invoice_date_key_strings, date_pattern)

# #     # Print extracted values
# #     print("PO Number Values:", po_number_values)
# #     print("Invoice Number Values:", invoice_number_values)
# #     print("PO Date Values:", po_date_values)
# #     print("Invoice Date Values:", invoice_date_values)

