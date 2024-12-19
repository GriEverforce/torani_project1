import re
import PyPDF2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

from constants import *
from app_logger import logger  



# Add more key strings as needed

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
    # Replace newline characters with a space
    text = text.replace('\n', ' ')
    return text

# Function to find key-value pairs in text
def find_key_values(text, key_strings, value_pattern):
    key_value_pairs = {}

    for key in key_strings:
        # Adjust regex to match key strings with optional whitespaces, case-insensitive, and consider lines with more spaces
        regex = rf"(?i){key}\s*[:#-]?\s*({value_pattern})"
        logger.info(f"key: '{key}' regex: {regex}")
        if key in text:
            logger.info(f"KEY({key}) found in TEXT:{text}")
        matches = re.findall(regex, text)
        if matches:
            logger.info(f"Found key: '{key}' in text: {text}")
            key_value_pairs[key] = matches[0]
    return key_value_pairs


def extract_value_from_pdf(pdf_path, key_string_list, required_pattern):

    # Path to your PDF file
    # pdf_path = 'repository_cfd/po-dir/email_body_po.pdf'

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Preprocess the text to handle spaces and newlines
    preprocessed_text = preprocess_text(pdf_text)

    key_pair = find_key_values(preprocessed_text, key_string_list, required_pattern)

    logger.info(f"key_pair: {key_pair}")

    key_value = 0
    if key_pair:
        key_list = list(key_pair.values())
        key_value = key_list[0]
   
    return key_value



# if __name__ == "__main__":
#     # Find key-value pairs
#     po_number_values = find_key_values(preprocessed_text, po_number_key_strings, number_pattern)
#     invoice_number_values = find_key_values(preprocessed_text, invoice_number_key_strings, number_pattern)
#     po_date_values = find_key_values(preprocessed_text, po_date_key_strings, date_pattern)
#     invoice_date_values = find_key_values(preprocessed_text, invoice_date_key_strings, date_pattern)

#     # Print extracted values
#     print("PO Number Values:", po_number_values)
#     print("Invoice Number Values:", invoice_number_values)
#     print("PO Date Values:", po_date_values)
#     print("Invoice Date Values:", invoice_date_values)

