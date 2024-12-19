import sys
import os
import argparse
import time
import logging




# Add the path to the 'features' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'features')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config')))
# print(f"sys.path: {sys.path}")

from get_ms_token import get_token
from get_ms_token import get_access_token_using_refresh_token, get_app_token
from scan_ms_email import get_emails
import constants
from app_logger import logger
from record_upload import connect_to_oracle
from record_upload import process_pdf_files
from app_settings import setup_folders



# def get_emails(access_token):
#     headers = {
#         'Authorization': f"Bearer {access_token}",
#         'Content-Type': 'application/json',
#     }
#     # Use the /users endpoint with the user ID or email address
#     user_id = 'cfd@torani.com'  # Replace with the actual user ID or email address
#     endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages'
#     response = requests.get(endpoint, headers=headers)

#     if response.status_code == 200:
#         messages = response.json()
#         for message in messages['value']:
#             print(f"Subject: {message['subject']}")
#             print(f"From: {message['from']['emailAddress']['address']}")
#             print(f"Body Preview: {message['bodyPreview']}")
#             print('-' * 40)
#     else:
#         print(f"Failed to fetch emails: {response.status_code}")
#         print(response.json())


def main(interval, stop_flag):
    print(f"Application started. Running every {interval} seconds. Create the file '{stop_flag}' to stop the program.")

    if os.path.exists(stop_flag):
        os.remove(stop_flag) # Rmove stop flag to start the application
    
    setup_folders()

    # Establish Oracle connection
    ora_conn = connect_to_oracle()
    if not ora_conn:
        logger.error("Oracle connection failed. Exiting...")
        exit(1)

    # # Needs login
    # access_token = get_token()

    # # Does not need login
    # access_token = get_access_token_using_refresh_token()

    # Gets access token with Application Persmission
    access_token = get_app_token()

    try:
        while True:
            # Check for stop flag
            if os.path.exists(stop_flag):
                logger.info(f"Stop flag '{stop_flag}' detected. Stopping application.")
                break
            
            # If we successfully obtained the access token, get and filter the emails
            if access_token:
                logger.info(f"Search strings in subject: {constants.MAIL_SEARCH_KEYWORDS}")
                emails = get_emails(access_token, constants.MAIL_SEARCH_KEYWORDS)
                # Set the base folder containing the PDF files

            repository_folder = constants.REPOSITORY_FOLDER

            # Process all PDF files and upload to the database
            process_pdf_files(repository_folder, ora_conn)

            if interval == -1: # Indicate not to loop. Run just once.
                break
            logger.info(f"Performing task at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"Sleeping for {interval} seconds .................................................")
            # Wait for the next interval
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Application interrupted manually. Exiting.")
    except Exception as e:
        logger.info(f"An error occurred: {e}")
    finally:
        logger.info("Application terminated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a task at regular intervals.")
    parser.add_argument("interval", type=int, help="Interval in seconds between each task. -1 indicate not to loop")
    parser.add_argument("--stop-flag", type=str, default="stop.flag", help="File name for the stop flag (default: stop.flag).")

    args = parser.parse_args()
    main(args.interval, args.stop_flag)
