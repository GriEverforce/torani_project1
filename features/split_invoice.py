import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
from app_logger import logger
from constants import *
from db_functions import insert_into_cfd_repository

import re
from PyPDF2 import PdfReader, PdfWriter
import os
from pathlib import Path

def extract_numbers(text):
    """
    Extract invoice and order numbers from text using regex
    Returns tuple of (invoice_number, order_number)
    """
    invoice_pattern = r"INVOICE\s*#\s*(\d+)"
    order_pattern = r"ORDER\s*#\s*(\d+)"
    
    invoice_match = re.search(invoice_pattern, text)
    order_match = re.search(order_pattern, text)
    
    invoice_num = invoice_match.group(1) if invoice_match else None
    order_num = order_match.group(1) if order_match else None
    
    return invoice_num, order_num

def get_invoice_info(page_text):
    """
    Get invoice information from a page, return None if no invoice numbers found
    """
    invoice_num, order_num = extract_numbers(page_text)
    if invoice_num and order_num:
        return {
            'invoice_num': invoice_num,
            'order_num': order_num
        }
    return None

def split_invoices(input_pdf_path, output_dir):
    logger.info(f"input_pdf_path: {input_pdf_path}, output_dir: {output_dir})")

    """
    Process PDF file containing multiple invoices and split into separate files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Open the PDF file
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    # Lists to store page groups
    page_groups = []
    current_group = None
    
    # First pass: group pages by invoice
    for page_num in range(total_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        invoice_info = get_invoice_info(text)
        
        if invoice_info:
            # Start new group if this is a new invoice
            if current_group is None or (
                invoice_info['invoice_num'] != current_group['invoice_info']['invoice_num'] or
                invoice_info['order_num'] != current_group['invoice_info']['order_num']
            ):
                if current_group:
                    page_groups.append(current_group)
                current_group = {
                    'invoice_info': invoice_info,
                    'pages': []
                }
            current_group['pages'].append(page_num)
        elif current_group:
            # Add page to current group if it's a continuation page
            current_group['pages'].append(page_num)
    
    # Add the last group
    if current_group:
        page_groups.append(current_group)
    
    # Second pass: create individual PDF files
    for group in page_groups:
        invoice_num = group['invoice_info']['invoice_num']
        order_num = group['invoice_info']['order_num']
        
        logger.info(f"writing invoice_num:{invoice_num} order_num: {order_num}")
        writer = PdfWriter()
        
        # Add all pages for this invoice
        for page_num in group['pages']:
            writer.add_page(reader.pages[page_num])
        
        # Save the invoice
        output_filename = f"{invoice_num}_{order_num}.pdf"
        output_file_path = output_path / output_filename
        
        with open(output_file_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Created: {output_filename} (Pages: {group['pages']})")




def upload_invoice_files(cursor, folder_path, attached_file_path, blob_file, upload_table):
    """
    Process files in the specified folder. If the file ends with .pdf, call insert().
    Otherwise, log an error message with the file name and type.

    :param folder_path: Path to the folder containing the files to process.
    """
    upload_ok = False

    logger.info(f"Split invoice folder : {folder_path}")
    # Check if folder exists
    if not os.path.exists(folder_path):
        logger.error( f"Folder does not exist: {folder_path}")
        return False
    
    logger.info(f"going to process -- Invoice folder_path: {folder_path} ")


    # Check if the folder is empty
    if not os.listdir(folder_path):
        folder_to_look_for = attached_file_path
        logger.info(f"Folder is empty: {folder_path}. So looking in to {folder_to_look_for}")
    else:
        folder_to_look_for = folder_path
        logger.info(f"Split Folder is Not empty: {folder_path}. Looking for PDF files inside split_invoices/")

    # Process files in the folder
    number_of_inv_file = 0
    for filename in os.listdir(folder_to_look_for):
        logger.info(f"processing -- Invoice file# {number_of_inv_file} in Split folder : {filename}")
        file_path = os.path.join(folder_to_look_for, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Check file extension
        if filename.lower().endswith('.pdf'):
            try:
                # Call the insert function for .pdf files
                upload_ok = insert_into_cfd_repository(cursor, f"{folder_to_look_for}/{filename}", filename, upload_table)
                logger.info(f"insert_into_cfd_repository() return upload_ok: {upload_ok}")
                if not upload_ok:
                    break
                number_of_inv_file +=1
            except Exception as e:
                logger.error(f"Error processing invocie file {filename}: {e}")
                upload_ok = False
        else:
            file_type = os.path.splitext(filename)[1] or "unknown"
            logger.error(f"Unsupported invoice file: {filename} (type: {file_type})")

    logger.info(f"DONE -- Invoice file# {number_of_inv_file} in Split folder : {filename}")
    return upload_ok


def process_invoice_documents(file_path, blob_file, cursor, upload_table):

    logger.info(f"file_path: {file_path} blob_file: {blob_file}")
    split_files_folder = f"{file_path}/{SPLIT_INVOICE_FOLDER}"
    split_invoices(f"{file_path}/{blob_file}", split_files_folder)
    result_to_return = upload_invoice_files(cursor, split_files_folder, file_path, blob_file, upload_table)

    return result_to_return


def main():
    # Configuration
    # input_pdf = "RTC_XML_Invoice_Print_Batch_of_061124.pdf"  # Change this to your input PDF path
    input_pdf = "multiple_invoices.pdf"  # Change this to your input PDF path
    output_directory = "split_invoices"  # Change this to your desired output directory

    try:
        process_invoices(input_pdf, output_directory)
        logger.info("Invoice processing completed successfully!")
    except Exception as e:
        logger.info(f"Error processing invoices: {str(e)}")

    logger.info(f"""\n=========\n \
Input PDF: {input_pdf} and Output files created in folder: {output_directory} \
            \n=========""")

if __name__ == "__main__":
    main()