import os
import sys
from datetime import datetime
import platform
import json
from pathlib import Path



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

# Our libraries
from env_utils import read_environment_variable
from constants import *
from app_logger import logger
# from file_parser import extract_value_from_pdf
from db_functions import connect_to_oracle
from db_functions import insert_into_cfd_repository
from split_bol import process_bol_documents
from split_invoice import process_invoice_documents



def find_json_file(folder_path):
    """
    This function searches for a .json file in the given folder.

    :param folder_path: Path to the folder where the search will occur.
    :return: The path of the first .json file found, or None if no .json file is found.
    """
    # Ensure the folder path is a valid directory
    if not os.path.isdir(folder_path):
        logger.error(f"Error: '{folder_path}' is not a valid directory.")
        return None

    # Iterate over all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file ends with .json extension
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            return json_file_path
    
    # If no .json file is found, return None
    return None

# # Example usage
# folder_path = '/path/to/your/folder'
# json_file = find_json_file(folder_path)

# if json_file:
#     print(f"Found JSON file: {json_file}")
# else:
#     print("No JSON file found in the given folder.")



def extract_header_info(file_path):
    try:
        with open(file_path, 'r') as file:
            headers = json.load(file)

        from_address = subject = date = None
        for header in headers:
            if header['name'].lower() == 'from':
                from_address = header['value']
            elif header['name'].lower() == 'subject':
                subject = header['value']
            elif header['name'].lower() == 'date':
                date = header['value']

        logger.info(f"from_address: {from_address} subject: {subject} date: {date}")
        return from_address, subject, date

    except Exception as e:
        print(f"Error reading the header file: {e}")
        return None, None, None

# # Example usage
# file_path = 'path_to_your_header_file.json'
# from_address, subject, date = extract_header_info(file_path)
# print(f"FROM: {from_address}")
# print(f"SUBJECT: {subject}")
# print(f"DATE: {date}")



def select_table_name(mail_subject):

    table_name = ''
    found_key_string = False
    # Convert subject to uppercase to make the search case insensitive
    subject_upper = mail_subject.upper()

    # Check for each key-string in the subject
    for key_string, table_name in key_string_to_table.items(): # key_string_to_table is defined in constants.py
        if key_string in subject_upper:
            found_key_string = True
            break # Table name found
    # if not table_name:
    if not found_key_string:
        logger.error(f"Mail subject has no document indiation string - {mail_subject}")
        table_name = ''
    else:
        logger.info(f"subject_upper: {subject_upper} table_name: {table_name}")
    logger.info(f"table_name: '{table_name}' for Subjec: '{subject_upper}'")
    return table_name

# Example usage
# mail_subject = "Your PO file is attached"
# table_name = select_table_name(mail_subject)
# print(f"Selected table name: {table_name}")


def get_num_from_doc(repository_table):

    # if repository_table == 'CFD_RTC_ORDER_PO_DOC':
    #     get_num_from_po()
    pass



def touch_file(directory, filename):
    # Create a Path object for the file
    file_path = Path(directory) / filename
    logger.info(f"Tocuhing>> file_path: '{file_path}'")
    # Touch the file (create if not exists, update timestamp if exists)
    try:
        file_path.touch(exist_ok=True)
        logger.info(f"File '{filename}' has been touched.")
    except Exception as e:
        logger.error(f"Error: {e}")

# # Example usage
# directory = '/path/to/your/directory'
# filename = 'example.txt'

# touch_file(directory, filename)



def process_pdf_files(pdf_file_folder, connection):
    """
    Read PDF files from the folder and subdirectories and upload them to Oracle.
    """
    cursor = connection.cursor()

    if not os.path.isdir(pdf_file_folder):
        logger.error(f"Blob files folder '{pdf_file_folder}' is not exisiting or not a folder")
    else:
        for file_in_folder in os.listdir(pdf_file_folder):
            path_and_file = os.path.join(pdf_file_folder, file_in_folder)
            # logger.info(f"path_and_file: {path_and_file}")
            if os.path.isdir(path_and_file):
                # What we found is a folder
                # Check if the folder blobs were already uploaded 
                if os.path.exists(os.path.join(path_and_file, BLOB_FILES_PROCESSED)):
                    # Blobs under this folder already processed
                    # logger.info(f"blob files already processed in '{path_and_file}'")
                    continue
                # Look for header and blob files inside this folder
                json_file = find_json_file(path_and_file) # looking for header file
                if not json_file:
                    logger.error(f"Header file (.json) for mail not found in the folder '{path_and_file}")
                    logger.error(f"TODO -- Need to send an alert email '{path_and_file}")
                    logger.error(f"ALERT> EMail header file missing. Notify support.")
                    continue
                    # TODO: This situation should not come. If it comes, we need to send ALERT EMAIL.
                logger.info(f"Header file found: {json_file}")    
            from_address, from_subject, from_date = extract_header_info(json_file)
            sub_dir = path_and_file
            for blob_file in os.listdir(sub_dir):
                logger.info(f"file '{blob_file}' found in folder '{sub_dir}'")
                # Based on the subject of the mail, know the documen type and decide the tablename
                upload_table = select_table_name(from_subject)
                if not upload_table:
                    logger.error(f"ALERT> Mail subject '{from_subject}' does not indicate document type")
                    logger.error(f"not uploading document received from from_address '{from_address}' & date '{from_date}'")
                    logger.error(f"TODO -- Need to send an alert email '{path_and_file}")

                    continue # Can't upload so skip this email message
                    # TODO: This situation should not come. If it comes, we need to send ALERT EMAIL.
                if blob_file.lower().endswith(".pdf"):
                    file_path = os.path.join(sub_dir, blob_file)
                    if "BOL" in blob_file.upper():
                        upload_ok = process_bol_documents(sub_dir, blob_file, cursor, upload_table)
                    elif "INVOICE" in blob_file.upper():
                        # upload_ok = process_invoices(file_path, f"{sub_dir}/{SPLIT_INVOICE_FOLDER}")
                        upload_ok = process_invoice_documents(sub_dir, blob_file, cursor, upload_table)
                    else: # PO or ORDER files
                        upload_ok = insert_into_cfd_repository(cursor, file_path, blob_file, upload_table)
                    if upload_ok:
                        # Blobs uploaded and so create marker file BLOB_FILES_PROCESSED
                        touch_file(sub_dir, BLOB_FILES_PROCESSED)
                    else:
                        logger.error(f"ALERT> Blob file {file_path} insert in table '{upload_table}' failed. Notify support.")

    connection.commit()
    cursor.close()

if __name__ == "__main__":
    # Set the base folder containing the PDF files
    base_folder = REPOSITORY_FOLDER

    # Establish Oracle connection
    conn = connect_to_oracle()
    try:
        # Process all PDF files and upload to the database
        process_pdf_files(base_folder, conn)
    finally:
        conn.close()
        logger.info("Database connection closed.")
