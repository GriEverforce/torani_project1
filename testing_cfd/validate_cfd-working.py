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

INV_TEMPLATE='invoice_template.docx'
INV_PREFIX='inv_'


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


def verify_test_data(connection, subject_of_the_mail, attachment_path):

    orcle_cursor = connection.cursor()
    tbl_name = select_table_name(subject_of_the_mail)
    if not tbl_name:
        logger.error(f"Subject of mail '{subject_of_the_mail}' is not indicating the dac type. Exiting...")
        exit(1)

    blob_filenam_column = get_column_name(constants.filename_column_names, tbl_name)
    # Get the latest record that was updated by this test program
    # sql_qry = f"SELECT {blob_filenam_column} FROM {tbl_name} ORDER BY CREATION_DATE DESC"
    sql_qry = f"SELECT {blob_filenam_column} from {tbl_name} ORDER BY CREATION_DATE DESC FETCH FIRST 1 ROWS ONLY"
    # qry_success, sql_response = exe_sql_query(orcle_cursor, sql_qry)
    logger.info(f"sql_qry: {sql_qry}")
    orcle_cursor.execute(sql_qry)
    data_from_tble = orcle_cursor.fetchone()
    if data_from_tble:
        fname_received = data_from_tble[0]
        fname = get_filename(attachment_path)
        # logger.info(f"latest filename for '{blob_filenam_column}' in the table '{tbl_name}': {orcle_cursor.fetchone()}")
        logger.info(f"latest record - '{blob_filenam_column}' in the table '{tbl_name}': {data_from_tble}")
        if fname_received == fname:
            logger.info(f"PASS: uploaded filename '{fname_received}' verfication")
            tst_passed = True
        else:
            logger.error(f"FAIL: uploaded filename '{fname_received}' not as expected '{fname}")
            tst_passed = False
    else:
        logger.error(f"Blob filename received from table '{tbl_name}' is '{data_from_tble}'")
        # logger.error(f"FAIL: uploaded filename '{fname_received}' not as expected '{fname}")
        tst_passed = False

    return tst_passed



def current_milli_time():
    return round(time.time() * 1000)

def main():
    if len(sys.argv) != 5:
        print("Usage: python send_email.py <subject> <attachment_path> <recipient_email> <verify>")
        sys.exit(1)

    subject = sys.argv[1]
    attachment_path = sys.argv[2]
    recipient_email = sys.argv[3]
    verify = sys.argv[4]

    files_to_send = 3

    orcle_connxion = connect_to_oracle()
    if not orcle_connxion:
        logger.error("Oracle connection failed. Exiting...")
        exit(1)

    for indx in range(files_to_send):
        output_file = f"{INV_PREFIX}_{str(current_milli_time())}"
        docx_files = output_file+'.docx'
        pdf_file = output_file+'.pdf'
        subject_of_mail = f"{subject} file attached {pdf_file}"
        # Generate sample PDF files
        replace_placeholders_in_word(INV_TEMPLATE, docx_files, pdf_file)

        logger.info(f"Generateed {files_to_send} files with prefix of '{INV_PREFIX}'")

        send_email(subject_of_mail, pdf_file, recipient_email)

        if verify in ['yes', 'Yes', 'YES']:
            logger.info("Waiting for 5 seconds before verifying.")
            time.sleep(5)
            pass_test = verify_test_data(orcle_connxion, subject, attachment_path)
            if not pass_test:
                logger.info("May be we need to wait for more time. So trying again after 5 seconds")
                time.sleep(5)
                pass_test = verify_test_data(orcle_connxion, subject, attachment_path)

if __name__ == "__main__":
    main()
