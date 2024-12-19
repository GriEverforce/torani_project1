import os
import sys
import time
import smtplib
from email.message import EmailMessage
import mimetypes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'features')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from constants import *
import constants
from db_functions import connect_to_oracle
from record_upload import select_table_name
from db_functions import get_column_name
from db_functions import exe_sql_query
from app_logger import logger
from generate_pdf import replace_placeholders_in_word



TEMPLATE_FILE_PATH = './templates_folder/'
GENERATED_FILE_PATH = './generated_files_folder/'
SUFFIX_TEMPLATE_FILE = '_template.docx'

DOC_TYPE_KEYWORDS = ["PO", "PURCHASE_ORDER", "PURCHASE ORDER", 'NEW ORDER', # PO
                        'ORDER', 'ORDER_ACKOWLEDEGMENT', 'ORDER_CONFIRMATION',  # ORDER
                        'PICKSLIP','PICK-SLIP', 'PICK_SLIP', # PICKSLIP
                        'BOL', 'BILL OF LADING', 'BILL-OF-LADING',# BOL
                        'INVOICE' # INVOICE
                        ]

# Define the mapping of key-strings in the mail subject to doc type
key_string_to_subject = {

        DOC_TYPE_KEYWORDS[0]: 'PO',
        DOC_TYPE_KEYWORDS[1]: 'PO',
        DOC_TYPE_KEYWORDS[2]: 'PO',
        DOC_TYPE_KEYWORDS[3]: 'PO',
        DOC_TYPE_KEYWORDS[4]: 'ORDER',
        DOC_TYPE_KEYWORDS[5]: 'ORDER',
        DOC_TYPE_KEYWORDS[6]: 'ORDER',
        DOC_TYPE_KEYWORDS[7]: 'PICKSLIP',
        DOC_TYPE_KEYWORDS[8]: 'PICKSLIP',
        DOC_TYPE_KEYWORDS[9]: 'PICKSLIP',
        DOC_TYPE_KEYWORDS[10]: 'BOL',
        DOC_TYPE_KEYWORDS[11]: 'BOL',
        DOC_TYPE_KEYWORDS[12]: 'BOL',
        DOC_TYPE_KEYWORDS[13]: 'INVOICE',
    }

def select_doc_key_string(doc_type):

    mail_subject_keystring = ''
    found_key_string = False
    # Convert subject to uppercase to make the search case insensitive
    doc_type_upper = doc_type.upper()

    # Check for each key-string in the doc_type
    for key_string, mail_subject_keystring in key_string_to_subject.items(): 
        if key_string in doc_type_upper:
            found_key_string = True
            break # mail_subject_keystring found
    # if not table_name:
    if not found_key_string:
        logger.error(f"Doc type entered has no document indiation string - {DOC_TYPE_KEYWORDS}")
        doc_type = ''
    else:
        logger.info(f"doc_type_upper: {doc_type_upper} doc_type: {mail_subject_keystring}")
    logger.info(f"doc_type: '{doc_type}' for mail_subject_keystring: '{mail_subject_keystring}'")
    return mail_subject_keystring


def send_email(subject, attachment_path, recipient_email):
    # Get Gmail credentials from environment variables
    gmail_user = os.getenv("SEND_EMAIL_USER")
    gmail_password = os.getenv("SEND_EMAIL_PWD")

    if not gmail_user or not gmail_password:
        logger.error("Error: Please set SEND_EMAIL_USER and SEND_EMAIL_USER in your environment variables.")
        sys.exit(1)

    # Create email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = recipient_email

    # Add email body
    msg.set_content("Please find the attached file.")

    # Attach file
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as file:
                mime_type, _ = mimetypes.guess_type(attachment_path)
                main_type, sub_type = mime_type.split('/')
                msg.add_attachment(file.read(), maintype=main_type, subtype=sub_type, filename=os.path.basename(attachment_path))
        except FileNotFoundError:
            logger.error(f"Error: File not found: {attachment_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error attaching file: {e}")
            sys.exit(1)

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
        logger.info(f"Email with subject '{subject}' to '{recipient_email}' sent successfully!")
    except Exception as e:
        logger.error(f"Email with subject '{subject}' to '{recipient_email}' - Exceptiopn: {e}")
        sys.exit(1)



def get_filename(path: str) -> str:
    # Use os.path.basename() to extract the filename from the path
    return os.path.basename(path)

# # Example usage:
# path = "<folder_name>/<folder_name>/filename"
# filename = get_filename(path)
# logger.info(filename)  # Output will be: 'filename'


def verify_test_data(connection, subject_of_the_mail, blob_fname):

    orcle_cursor = connection.cursor()
    tbl_name = select_table_name(subject_of_the_mail)
    if not tbl_name:
        logger.error(f"Subject of mail '{subject_of_the_mail}' is not indicating the dac type. Exiting...")
        exit(1)

    blob_filenam_column = get_column_name(constants.filename_column_names, tbl_name)
    tbl_name = select_table_name(subject_of_the_mail)
    fname_column = get_column_name(constants.filename_column_names, tbl_name)
    # Get the latest record that was updated by this test program
    # sql_qry = f"SELECT {blob_filenam_column} FROM {tbl_name} ORDER BY CREATION_DATE DESC"
    # sql_qry = f"SELECT {blob_filenam_column} from {tbl_name} ORDER BY CREATION_DATE DESC FETCH FIRST 1 ROWS ONLY"
    # Sample query: SELECT INVOICE_FILE_NAME from CFD_RTC_ORDER_INVOICE_DOC WHERE INVOICE_FILE_NAME='inv__1733900787385.pdf';
    sql_qry = f"SELECT {fname_column} from {tbl_name} WHERE {blob_filenam_column}='{blob_fname}'"
    # qry_success, sql_response = exe_sql_query(orcle_cursor, sql_qry)
    logger.info(f"sql_qry: {sql_qry}")
    orcle_cursor.execute(sql_qry)
    data_from_tble = orcle_cursor.fetchone()
    if data_from_tble:
        fname_received = data_from_tble[0]
        # logger.info(f"latest filename for '{blob_filenam_column}' in the table '{tbl_name}': {orcle_cursor.fetchone()}")
        logger.info(f"latest record - '{blob_filenam_column}' in the table '{tbl_name}': {data_from_tble}")
        if fname_received == blob_fname:
            logger.info(f"PASS: uploaded filename '{fname_received}' in table '{tbl_name}' verfication")
            tst_passed = True
        else:
            logger.error(f"FAIL: uploaded filename '{fname_received}' not as expected '{blob_fname} in table '{tbl_name}'")
            tst_passed = False
    else:
        logger.error(f"FAIL: Blob file '{blob_fname}' not uploaded correctly in table '{tbl_name}'. Received '{data_from_tble}'")
        tst_passed = False

    return tst_passed



def current_milli_time():
    return round(time.time() * 1000)


def decide_subject_of_mail(doc_type): # Not used
    mail_subject = ''
    if doc_type.upper in ['PO', 'PURCHASE ORDER', 'PURCHASE_ORDER']:
        mail_subject = "PO "
    elif doc_type.upper in ['ORDER', 'ORDER CONFIRMATION', 'ORDER ACKNOWLEDEMENT']:
        mail_subject = "ORDER "
    elif doc_type.upper in ['PICKSLIP', 'PICK SLIP', 'PICK_SLIP']:
        mail_subject = "PICKSLIP "
    elif doc_type.upper in ['BOL', 'BILL OF LADING ', 'SIGNED BOL']:
        mail_subject = "BOL "
    elif doc_type.upper in ['INVOICE']:
        mail_subject = "INVOICE"
    else:
        logger.error(f"Invalid document type '{doc_type}' entered")
        logger.info()
    return mail_subject


def main():
    if len(sys.argv) != 5:
        print("Usage: python send_email.py <doc_type> <recipient_email> <number_of_mails> <verify>")
        print('Example: python send_email.py "INVOICE" 3 email@email.com yes')
        sys.exit(1)

    doc_type = sys.argv[1]
    recipient_email = sys.argv[2]
    files_to_send = sys.argv[3]
    verify = sys.argv[4]

    doc_key_str = select_doc_key_string(doc_type)
    mandetory_space = ' '

    logger.info(f"doc_key_str: {doc_key_str}")
    orcle_connxion = connect_to_oracle()
    if not orcle_connxion:
        logger.error("Oracle connection failed. Exiting...")
        exit(1)

    for indx in range(int(files_to_send)):
        output_file = f"{doc_key_str}_{str(current_milli_time())}"
        docx_files = f"{GENERATED_FILE_PATH}/{output_file}.docx"
        pdf_file = f"{GENERATED_FILE_PATH}/{output_file}.pdf"
        subject_of_mail = f"{doc_key_str}{mandetory_space}-attached-{output_file}.pdf"
        template_file_with_path = f"{TEMPLATE_FILE_PATH}/{doc_key_str}{SUFFIX_TEMPLATE_FILE}"
        logger.info(f"output_file: {output_file} docx_files:{docx_files} pdf_file: {pdf_file} subject_of_mail:{subject_of_mail}") 
        # Generate sample PDF files
        replace_placeholders_in_word(template_file_with_path, docx_files, pdf_file)

        logger.info(f"{(indx+1)}> Generated file '{pdf_file}'")

        send_email(subject_of_mail, pdf_file, recipient_email)

        sleep_time = 30
        sleep_time2 = 20
        if verify in ['yes', 'Yes', 'YES']:
            logger.info(f"Waiting for {sleep_time} seconds before verifying.")
            time.sleep(sleep_time)
            pass_test = verify_test_data(orcle_connxion, subject_of_mail, pdf_file)
            if not pass_test:
                logger.info(f"May be we need to wait for more time. So trying again after {sleep_time2} seconds")
                time.sleep(sleep_time2)
                pass_test = verify_test_data(orcle_connxion, subject_of_mail, pdf_file)

if __name__ == "__main__":
    main()
