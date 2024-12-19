import os
import sys
import smtplib
from email.message import EmailMessage
import mimetypes
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './features')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from features.constants import *
from db_functions import connect_to_oracle
from record_upload import select_table_name
from db_functions import get_column_name
from db_functions import exe_sql_query
from app_logger import logger


def send_email(subject, attachment_path, recipient_email):
    # Get Gmail credentials from environment variables
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")

    if not gmail_user or not gmail_password:
        print("Error: Please set GMAIL_USER and GMAIL_PASSWORD in your environment variables.")
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
            print(f"Error: File not found: {attachment_path}")
            sys.exit(1)
        except Exception as e:
            print(f"Error attaching file: {e}")
            sys.exit(1)

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        sys.exit(1)

def verify_test_data(subject_of_the_mail):

    connxion = connect_to_oracle()
    tbl_name = select_table_name(subject_of_the_mail)
    blob_column = get_column_name(constants.blob_column_names, constants.upload_repository_table)
    sql_qry = f"SELECT {blob_column} FROM {tbl_name}"
    qry_success, sql_response = exe_sql_query(connxion.cursor, sql_qry)
    if qry_success:
        logger.info(f"sql_response: {sql_response}")




def main():
    if len(sys.argv) != 4:
        print("Usage: python send_email.py <subject> <attachment_path> <recipient_email>")
        sys.exit(1)

    subject = sys.argv[1]
    attachment_path = sys.argv[2]
    recipient_email = sys.argv[3]

    send_email(subject, attachment_path, recipient_email)

    verify_test_data(subject)

if __name__ == "__main__":
    main()
