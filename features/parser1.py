import re
import PyPDF2

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
    key_value_pairs = {}
    lines = text.split(' NEWLINE ')
    for i, line in enumerate(lines):
        for key in key_strings:
            # First try to find the value on the same line
            regex = rf"(?i){key}\s*[:#-]?\s*({value_pattern})"
            match = re.search(regex, line)
            if match:
                key_value_pairs[key] = match.group(1)
            else:
                # If not found, check the next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    match = re.search(value_pattern, next_line)
                    if match:
                        key_value_pairs[key] = match.group(0)
    return key_value_pairs

# Main function to extract key-value pairs
def extract_key_value_pairs(pdf_path, key_string_dict):
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Preprocess the text to handle spaces and newlines
    preprocessed_text = preprocess_text(pdf_text)
    
    # Dictionary to hold all extracted key-value pairs
    all_key_values = {}
    
    # Iterate through the dictionary of key strings and their patterns
    for keys, pattern in key_string_dict.items():
        key_value_pairs = find_key_values(preprocessed_text, keys, pattern)
        all_key_values.update(key_value_pairs)
    
    return all_key_values

# Define patterns for dates
date_pattern = r'\d{1,2}-[a-zA-Z]{3}-\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{4}-\d{1,2}-\d{1,2}'

# Sample usage
key_string_dict = {
    ('PO', 'PO Number', 'Purchase Order'): r'\d+',
    ('Invoice Number', 'Invoice #', 'Invoice:', 'Inv. No.'): r'\d+',
    ('PO Date', 'Purchase Order Date', 'PO Dt.'): date_pattern,
    ('DATE', 'Invoice Dt.'): date_pattern
}

pdf_path = 'invoice_1_of_1.pdf'
extracted_values = extract_key_value_pairs(pdf_path, key_string_dict)
print(extracted_values)

