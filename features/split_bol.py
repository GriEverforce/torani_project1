import PyPDF2
import re
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
from app_logger import logger
from constants import *
from db_functions import insert_into_cfd_repository
from app_settings import check_and_create_folder




def rename_file(folder_path, old_filename, new_filename):
    """
    Renames a file in the specified folder.

    :param folder_path: Path to the folder where the file is located.
    :param old_filename: Current name of the file to be renamed.
    :param new_filename: New name for the file.
    :return: None
    """
    # Construct the full file paths
    old_file_path = os.path.join(folder_path, old_filename)
    new_file_path = os.path.join(folder_path, new_filename)

    # Check if the old file exists
    if not os.path.exists(old_file_path):
        print(f"Error: The file '{old_filename}' does not exist in the specified folder.")
        return

    # Check if a file with the new name already exists
    if os.path.exists(new_file_path):
        print(f"Error: A file with the name '{new_filename}' already exists.")
        return

    try:
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"File renamed from '{old_filename}' to '{new_filename}' successfully.")
    except Exception as e:
        print(f"Error renaming file: {e}")

# # Example usage:
# folder_path = "/path/to/your/folder"
# old_filename = "old_file.txt"
# new_filename = "new_file.txt"



def process_bol_documents(pdf_file_path, name_pdf_file, cursor, upload_table):
    def save_pdf(writer, filename):
        with open(filename, 'wb') as out_file:
            writer.write(out_file)

    # Read the input PDF file
    pdf_path_and_file = os.path.join(pdf_file_path, name_pdf_file)
    reader = PyPDF2.PdfReader(pdf_path_and_file)
    num_pages = len(reader.pages)
    bol_docs = []
    current_bol = []

    # Regular expression to identify BOL document start (e.g., BOL#)
    bol_pattern = re.compile(r'BOL\s*#\s*(\d+)')

    # It could be multiple BOL files. Try to split them.
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()

        # Check for the BOL pattern in the page text
        match = bol_pattern.search(text)
        if match:
            if current_bol:
                bol_docs.append(current_bol)
                current_bol = []
        current_bol.append(page)
    
    if current_bol:
        bol_docs.append(current_bol)

    number_of_bol_files = 0
    logger.info(f"Number of BOL documents: {len(bol_docs)}")
    if len(bol_docs) > 1: # Many BOL in a single file. Split them
        # Save each BOL document as a separate PDF file
        for index, bol_doc in enumerate(bol_docs):
            writer = PyPDF2.PdfWriter()
            for page in bol_doc:
                writer.add_page(page)
            bol_number = index + 1
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_filename = f'{date_str}_BOL{bol_number}.pdf'
            bol_split_path = os.path.join(pdf_file_path, SPLIT_BOL_FOLDER)
            check_and_create_folder(bol_split_path)
            path_and_file = os.path.join(bol_split_path, output_filename)
            save_pdf(writer, path_and_file)
            logger.info(f'{number_of_bol_files} BOL document saved as {path_and_file}')
            number_of_bol_files +=1
    else:
        logger.info("Single BOL and so not splitting")

    if number_of_bol_files > 1: # It is not a single file
        # Rename the original file and process the newly created file
        new_filename = f"{name_pdf_file}_orginal_bol_file"
        rename_file(pdf_file_path, name_pdf_file, new_filename)
        number_of_bol_files = 0
        for blob_file in os.listdir(bol_split_path):
            pdf_with_path = os.path.join(bol_split_path, blob_file)
            logger.info(f'{number_of_bol_files}> Uploading BOL document {pdf_with_path}')
            upload_ok = insert_into_cfd_repository(cursor, pdf_with_path, blob_file, upload_table)
            if not upload_ok:
                break
            number_of_bol_files +=1
    else:
        # Process the single file
        # There is no split file. So remove the split folder if created
        pdf_with_path = os.path.join(pdf_file_path, name_pdf_file)
        logger.info(f'{number_of_bol_files}> Uploading BOL document {pdf_with_path}')
        upload_ok = insert_into_cfd_repository(cursor, pdf_with_path, name_pdf_file, upload_table)

    return upload_ok

# # Example usage
# pdf_file_path = 'repository_cfd/bol-dir/multi_bol.pdf'
# split_bol_documents(pdf_file_path)
