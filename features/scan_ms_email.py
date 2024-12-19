import requests
from msal import PublicClientApplication
import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

# Our libraries
# from .get_ms_token import get_token
from constants import *
from app_logger import logger  
from body_email import save_email_body_to_pdf
# from body_email import save_email_as_pdf_gbt

import os
import requests
import re
from msal import PublicClientApplication


# Add the path to the directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import constants


# List of search strings and email addresses
# ["PO", "ORDER", "PURCHASE ORDER", 'PO', 'BOL', 'BILL OF LADING', 'INVOICE']
EMAIL_ADDRESSES = ['example1@domain.com', 'example2@domain.com']  # Add your specific email addresses

# Base directory for attachments
REPOSITORY_DIR = constants.REPOSITORY_FOLDER

def sanitize_subject(subject):
    # Remove invalid characters for directory names
    return re.sub(r'[<>:"/\\|?*]', '', subject)

def download_attachment(user_id, access_token, message_id, attachment_id, attachment_name, sanitized_subject):
    # Download only .pdf files
    if not attachment_name.lower().endswith('.pdf'):
        return
    
    # endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}/attachments/{attachment_id}/$value' # Read with Application Permission
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        # Create directory for the specific message ID with combination of subject and message id
        mail_dir = os.path.join(REPOSITORY_DIR, sanitized_subject[:50] + '_' + message_id[:20])
        os.makedirs(mail_dir, exist_ok=True)
        attachment_path = os.path.join(mail_dir, attachment_name)

        # Save the attachment to the directory
        with open(attachment_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"Downloaded attachment: {attachment_path}")
        download_success = True
    else:
        logger.error(f"Failed to download attachment: {response.status_code}")
        logger.info(response.json())
        download_success = False

    return download_success, mail_dir


def get_email_headers_and_save(user_id, access_token, message_id, save_directory):
    
    # endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}?$select=internetMessageHeaders"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}?$select=internetMessageHeaders' # Read with Application Permission

    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        message = response.json()
        headers = message.get('internetMessageHeaders', [])
        # Save headers to JSON file
        headers_file_path = os.path.join(save_directory, f"{message_id[0]}_headers.json")
        with open(headers_file_path, 'w') as file:
            json.dump(headers, file, indent=4)
        logger.info(f"Saved headers to {headers_file_path}")
    else:
        logger.error(f"Failed to fetch email headers: {response.status_code}")
        logger.error(response.json())


# Mark an email as read
def old_mark_as_read(access_token, email_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
    
    # Data to mark the email as read
    data = {
        "isRead": True
    }
    
    # Headers for the request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Send the PATCH request to mark the email as read
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        logger.info(f"Email with ID {email_id} marked as read.")
    else:
        logger.info(f"Error marking email as read: {response.status_code}")



def check_body_has_purchase_data(uid, message, message_id, access_token, subject, sanitized_subject):

    def check_at_least_one_word_in_string(s, words):
        return any(word in s for word in words) # Using any() for At Least One Word Match

    if check_at_least_one_word_in_string(subject, PO_KEY_WOPDS):
        logger.info(f"Subject is '{subject}' but no attachement. So reading the body as PO")
        # Create directory for the specific message ID with combination of subject and message id
        mail_dir = os.path.join(REPOSITORY_DIR, sanitized_subject[:50] + '_' + access_token[:20])
        os.makedirs(mail_dir, exist_ok=True)
        email_body_file_path = os.path.join(mail_dir, EMAIL_BODY_PO_PDF_FILE)
        logger.info(f"email_body_file_path: {email_body_file_path} mail_dir: {mail_dir}")
        save_email_body_to_pdf(message, email_body_file_path)
        get_email_headers_and_save(uid, access_token, message_id, mail_dir)

        # Once testing completed, this can be removed
        allow_repeat_mails(mail_dir, subject)



def mark_the_mail_as_read(user_id, sub_ject, message_id, access_token):
    try:
        # url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
        url = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}' # Read with Application Permission

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "isRead": True
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"Email '{sub_ject}' marked as read.")
        else:
            logger.error(f"Failed to mark email '{sub_ject}' as read. Error: {response.status_code}")
    except Exception as mail_err:
        logger.error(f"Exception while marking as read - {mail_err}")


def allow_repeat_mails(mail_folder, subject):
    # We might have received the mail again, with the same subject.
    # So if there is a file BLOB_FILES_PROCESSED, remove it.
    # This may not happen normally but during testing, we may repeat the mails.

    processed_indicator = os.path.join(mail_folder, BLOB_FILES_PROCESSED)
    if os.path.exists(processed_indicator):
        logger.info(f"REPEAT EMail [Subject: {subject}]-removing BLOB_FILES_PROCESSED")
        os.remove(processed_indicator) 


def get_emails(access_token, serach_keywords):
    # Fetch top 80 emails ordered by received date in descending order
    top_count = 2
    read_only_new_mails = "isRead eq false"
    # endpoint = f"https://graph.microsoft.com/v1.0/me/messages?$top={top_count}&$orderby=receivedDateTime desc"
    endpoint = f"https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$top={top_count}"
    # endpoint = f"https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$filter={read_only_new_mails}&$top={top_count}" # Read with Delegated Permission

    user_id = 'cfd@torani.com'  # Replace with the actual user ID or email address
    # endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages?$top={top_count}' # Read with Application Permission
    endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/Inbox/messages?$filter={read_only_new_mails}&$top={top_count}" # Read with Delegated Permission

    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(endpoint, headers=headers)
    mails_with_search_keyworkds = 0
    if response.status_code == 200:
        messages = response.json()
        if len(messages['value']):
            logger.info(f"Number of email messages read: {len(messages['value'])}")
        else:
            logger.info("-- There is no new mail received --")
    
        for message in messages['value']:
            subject = message['subject']
            sanitized_subject = sanitize_subject(subject)
            from_address = message['from']['emailAddress']['address']
            message_id = message['id']
            # logger.info(f"Subject: {subject}")
            # logger.info(f"From: {from_address}")
            # logger.info(f"ID: {message_id}")
            # logger.info(f"serach_keywords: {serach_keywords}")
            # Apply filtering in code

            if any(s in subject for s in serach_keywords) or from_address in EMAIL_ADDRESSES:
                mails_with_search_keyworkds += 1
                mark_the_mail_as_read(user_id, subject, message_id, access_token)
                # Check for attachments
                # attachments_endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
                attachments_endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}/attachments' # Read with Application Permission

                attachments_response = requests.get(attachments_endpoint, headers=headers)
                if attachments_response.status_code == 200:
                    attachments = attachments_response.json()
                    if attachments['value']:
                        pdf_found = False
                        for attachment in attachments['value']:
                            logger.info(f"keywords found in subject. Attachement found: {attachment['@odata.type'] == '#microsoft.graph.fileAttachment'}")
                            if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
                                attachment_id = attachment['id']
                                attachment_name = attachment['name']
                                if attachment_name.lower().endswith('.pdf'):            
                                    logger.info(f"From: {from_address} Subject: {subject}")
                                    good_download, mail_folder = download_attachment(user_id, access_token, message_id, attachment_id, attachment_name, sanitized_subject)
                                    if good_download:
                                        pdf_found = True
                                        logger.info(f"Subject: {subject}, PDF attachment found **")
                                        get_email_headers_and_save(user_id, access_token, message_id, mail_folder)
                                        # TODO: Mark each email as read after displaying it
                                        # For now let us change status as we not using the dedicated email id
                                        # mark_as_read(access_token, message_id) --DONE
                                        allow_repeat_mails(mail_folder, subject)
                                    else:
                                        logger.error(f"Attachment file ('{attachment_name}') download error ")
                        if not pdf_found:
                            logger.info(f"Subject: {subject}, No PDF attachment")
                            check_body_has_purchase_data(message, message_id, access_token, subject, sanitized_subject)
                    else:
                        logger.info(f"Subject: {subject}, No attachment")
                        check_body_has_purchase_data(message, message_id, access_token, subject, sanitized_subject)
                else:
                    logger.info(f"Failed to fetch attachments: {attachments_response.status_code}")
                    logger.info(attachments_response.json())
            # logger.info('-' * 40)
    else:
        logger.info(f"Failed to fetch emails: {response.status_code}")
        logger.info(response.json())

    if mails_with_search_keyworkds:
        logger.info(f"Number of emails with keywords in the subject: {mails_with_search_keyworkds}")
    else:
        logger.info("-- No email received with the keywords in the subject --")

        
# try:
#     token = get_token()
#     get_emails(token)
# except ValueError as e:
#     logger.info(e)

