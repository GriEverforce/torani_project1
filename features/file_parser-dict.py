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
    # Replace newline characters with a space
    text = text.replace('\n', ' ')
    return text

# Function to find key-value pairs in text
def find_key_values(text, key_strings, value_pattern):
    key_value_pairs = {}
    for key in key_strings:
        # Adjust regex to match key strings with optional whitespaces, case-insensitive, and consider lines with more spaces
        regex = rf"(?i){key}\s*[:#-]?\s*({value_pattern})"
        matches = re.findall(regex, text)
        if matches:
            key_value_pairs[key] = matches[0]
    return key_value_pairs

# Main function to extract key-value pairs
def extract_value_from_pdf(pdf_path, key_string_dict):
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Preprocess the text to handle spaces and newlines
    preprocessed_text = preprocess_text(pdf_text)
    
    # Dictionary to hold all extracted key-value pairs
    all_key_values = {}
    
    # Iterate through the dictionary of key strings and their patterns
    for key, pattern in key_string_dict.items():
        key_value_pairs = find_key_values(preprocessed_text, key, pattern)
        all_key_values.update(key_value_pairs)
    
    return all_key_values


if __name__ == "__main__":
    # Sample usage
    key_string_dict = {
        ('PO', 'PO Number', 'Purchase Order'): r'\d+',
        ('Invoice Number', 'Invoice #', 'Invoice:', 'Inv. No.'): r'\d+',
        ('PO Date', 'Purchase Order Date', 'PO Dt.'): r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{1,2}-\d{1,2}',
        ('Invoice Date', 'Invoice Dt.'): r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{1,2}-\d{1,2}'
    }

    pdf_path = 'repository_cfd/po-dir/email_body_po.pdf'
    extracted_values = extract_value_from_pdf(pdf_path, key_string_dict)
    print(extracted_values)

