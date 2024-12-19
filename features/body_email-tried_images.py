# import msal
# import requests
# from bs4 import BeautifulSoup
# import pdfkit
# from datetime import datetime
# import os
# import urllib
# import base64

# # # Replace these with your actual values
# # CLIENT_ID = 'your-client-id'
# # CLIENT_SECRET = 'your-client-secret'
# # TENANT_ID = 'your-tenant-id'

# # # Authority and scopes
# # AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# # SCOPES = ["https://graph.microsoft.com/.default"]

# import msal
# import requests
# from bs4 import BeautifulSoup
# import pdfkit
# from datetime import datetime
# import os
# import urllib.parse

# # # Replace these with your actual values
# # CLIENT_ID = 'your-client-id'
# # CLIENT_SECRET = 'your-client-secret'
# # TENANT_ID = 'your-tenant-id'

# # # Authority and scopes
# # AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# # SCOPES = ["https://graph.microsoft.com/.default"]

# # def get_access_token():
# #     app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
# #     result = app.acquire_token_for_client(scopes=SCOPES)
# #     if "access_token" in result:
# #         return result["access_token"]
# #     else:
# #         raise Exception("Could not obtain access token")

# def download_image(url, local_path):
#     print("Downloading image: ")
#     try:
#         response = requests.get(url, stream=True)
#         if response.status_code == 200:
#             with open(local_path, 'wb') as f:
#                 for chunk in response.iter_content(1024):
#                     f.write(chunk)
#             return True
#     except Exception as e:
#         print(f"Failed to download image from {url}: {e}")
#     return False

# # def extract_emails_to_pdf(subject_keywords):
# #     token = get_access_token()
# #     headers = {"Authorization": f"Bearer {token}"}
    
# #     # API endpoint to get emails
# #     url = "https://graph.microsoft.com/v1.0/me/messages"
    
# #     # Request the emails
# #     response = requests.get(url, headers=headers)
# #     emails = response.json().get('value', [])
    
# #     for email in emails:
# #         if any(keyword in email['subject'].upper() for keyword in subject_keywords):
# #             # Check if email has no attachments
# #             if not email['hasAttachments']:
# #                 save_email_body_to_pdf(email)

# def save_email_body_to_pdf(email, pdf_filename):
#     body = email['body']['content']
#     subject = email['subject']
#     from_email = email['from']['emailAddress']['address']
#     to_emails = ", ".join([recipient['emailAddress']['address'] for recipient in email['toRecipients']])
#     received_time = email['receivedDateTime'][:10]  # Format YYYY-MM-DD

#     # # Generate PDF file name
#     # pdf_filename = f'{received_time}_{subject}.pdf'
    
#     # Create a directory for images
#     images_dir = "email_images"
#     os.makedirs(images_dir, exist_ok=True)
    
#     # Parse the email body
#     soup = BeautifulSoup(body, "html.parser")
    
#     # Download and replace image URLs with local paths
#     for img in soup.find_all('img'):
#         img_url = img.get('src')
#         if img_url:
#             parsed_url = urllib.parse.urlparse(img_url)
#             if not parsed_url.scheme:
#                 img_url = urllib.parse.urljoin("https://base.url.of.your.email.server", img_url)
#             img_filename = os.path.join(images_dir, os.path.basename(parsed_url.path))
#             if download_image(img_url, img_filename):
#                 img['src'] = img_filename
#             else:
#                 # Handle embedded images (cid:ii_m47gc3l70)
#                 if img_url.startswith('cid:'):
#                     img_id = img_url.split(':')[1]
#                     img_data = email['body']['attachments'][img_id]['contentBytes']
#                     with open(img_filename, 'wb') as f:
#                         f.write(base64.b64decode(img_data))
#                     img['src'] = img_filename

#     # Create HTML content with email metadata
#     html_content = f"""
#     <html>
#     <head>
#         <meta charset="UTF-8">
#     </head>
#     <body>
#         <p><strong>From:</strong> {from_email}</p>
#         <p><strong>To:</strong> {to_emails}</p>
#         <p><strong>Subject:</strong> {subject}</p>
#         <p><strong>Date:</strong> {received_time}</p>
#         <hr>
#         {str(soup)}
#     </body>
#     </html>
#     """
    
#     # Convert HTML to PDF
#     options = {
#         'enable-local-file-access': None
#     }
#     try:
#         pdfkit.from_string(html_content, pdf_filename, options=options)
#         print(f'PDF saved as {pdf_filename}')
#     except IOError as e:
#         print(f"Error saving email as PDF: {e}")

# # # Example usage
# # PO_KEY_WORDS = [' PO ', ' PURCHASE ORDER', ' PURCHASE_ORDER']
# # extract_emails_to_pdf(PO_KEY_WORDS)


# import msal
# import requests
# from bs4 import BeautifulSoup
# import pdfkit
# from datetime import datetime
# import os
# import urllib.parse
# import base64

# # # Replace these with your actual values
# # CLIENT_ID = 'your-client-id'
# # CLIENT_SECRET = 'your-client-secret'
# # TENANT_ID = 'your-tenant-id'

# # # Authority and scopes
# # AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# # SCOPES = ["https://graph.microsoft.com/.default"]

# # def get_access_token():
# #     app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
# #     result = app.acquire_token_for_client(scopes=SCOPES)
# #     if "access_token" in result:
# #         return result["access_token"]
# #     else:
# #         raise Exception("Could not obtain access token")

# def download_image(url, local_path):
#     try:
#         response = requests.get(url, stream=True)
#         if response.status_code == 200:
#             with open(local_path, 'wb') as f:
#                 for chunk in response.iter_content(1024):
#                     f.write(chunk)
#             return True
#     except Exception as e:
#         print(f"Failed to download image from {url}: {e}")
#     return False

# # def extract_emails_to_pdf(subject_keywords):
# #     token = get_access_token()
# #     headers = {"Authorization": f"Bearer {token}"}
    
# #     # API endpoint to get emails
# #     url = "https://graph.microsoft.com/v1.0/me/messages"
    
# #     # Request the emails
# #     response = requests.get(url, headers=headers)
# #     emails = response.json().get('value', [])
    
# #     for email in emails:
# #         if any(keyword in email['subject'].upper() for keyword in subject_keywords):
# #             # Check if email has no attachments
# #             if not email['hasAttachments']:
# #                 save_email_body_to_pdf(email, token)

# def save_email_body_to_pdf(email, token, odf_fikname):
#     body = email['body']['content']
#     subject = email['subject']
#     from_email = email['from']['emailAddress']['address']
#     to_emails = ", ".join([recipient['emailAddress']['address'] for recipient in email['toRecipients']])
#     received_time = email['receivedDateTime'][:10]  # Format YYYY-MM-DD

#     # # Generate PDF file name
#     # pdf_filename = f'{received_time}_{subject}.pdf'
    
#     # Create a directory for images
#     images_dir = "email_images"
#     os.makedirs(images_dir, exist_ok=True)
    
#     # Parse the email body
#     soup = BeautifulSoup(body, "html.parser")
    
#     # Download and replace image URLs with local paths
#     for img in soup.find_all('img'):
#         img_url = img.get('src')
#         if img_url:
#             parsed_url = urllib.parse.urlparse(img_url)
#             if not parsed_url.scheme:
#                 img_url = urllib.parse.urljoin("https://base.url.of.your.email.server", img_url)
#             img_filename = os.path.join(images_dir, os.path.basename(parsed_url.path))
#             if download_image(img_url, img_filename):
#                 img['src'] = img_filename
#             else:
#                 # Handle embedded images (cid:ii_m47gc3l70)
#                 if img_url.startswith('cid:'):
#                     img_id = img_url.split(':')[1]
#                     img_content = get_attachment(email['id'], img_id, token)
#                     if img_content:
#                         with open(img_filename, 'wb') as f:
#                             f.write(base64.b64decode(img_content))
#                         img['src'] = img_filename

# def get_attachment(message_id, attachment_id, token):
#     url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value"
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.content
#     return None

#     # Create HTML content with email metadata
#     html_content = f"""
#     <html>
#     <head>
#         <meta charset="UTF-8">
#     </head>
#     <body>
#         <p><strong>From:</strong> {from_email}</p>
#         <p><strong>To:</strong> {to_emails}</p>
#         <p><strong>Subject:</strong> {subject}</p>
#         <p><strong>Date:</strong> {received_time}</p>
#         <hr>
#         {str(soup)}
#     </body>
#     </html>
#     """
    
#     # Convert HTML to PDF
#     options = {
#         'enable-local-file-access': None
#     }
#     try:
#         pdfkit.from_string(html_content, pdf_filename, options=options)
#         print(f'PDF saved as {pdf_filename}')
#     except IOError as e:
#         print(f"Error saving email as PDF: {e}")

# # # Example usage
# # PO_KEY_WORDS = [' PO ', ' PURCHASE ORDER', ' PURCHASE_ORDER']
# # extract_emails_to_pdf(PO_KEY_WORDS)


# -----------------------------------

import msal
import requests
from bs4 import BeautifulSoup
import pdfkit
from datetime import datetime
import os
import urllib.parse
import base64

# # Replace these with your actual values
# CLIENT_ID = 'your-client-id'
# CLIENT_SECRET = 'your-client-secret'
# TENANT_ID = 'your-tenant-id'

# # Authority and scopes
# AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# SCOPES = ["https://graph.microsoft.com/.default"]

# def get_access_token():
#     app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
#     result = app.acquire_token_for_client(scopes=SCOPES)
#     if "access_token" in result:
#         return result["access_token"]
#     else:
#         raise Exception("Could not obtain access token")

def download_image(url, local_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
    return False

def get_attachment(message_id, token):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('value', [])
    return []

# def extract_emails_to_pdf(subject_keywords):
#     token = get_access_token()
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # API endpoint to get emails
#     url = "https://graph.microsoft.com/v1.0/me/messages"
    
#     # Request the emails
#     response = requests.get(url, headers=headers)
#     emails = response.json().get('value', [])
    
#     for email in emails:
#         if any(keyword in email['subject'].upper() for keyword in subject_keywords):
#             # Check if email has no attachments
#             if not email['hasAttachments']:
#                 save_email_body_to_pdf(email, token)

def save_email_body_to_pdf(email, token, pdf_filename):
    body = email['body']['content']
    subject = email['subject']
    from_email = email['from']['emailAddress']['address']
    to_emails = ", ".join([recipient['emailAddress']['address'] for recipient in email['toRecipients']])
    received_time = email['receivedDateTime'][:10]  # Format YYYY-MM-DD

    # # Generate PDF file name
    # pdf_filename = f'{received_time}_{subject}.pdf'
    
    # Create a directory for images
    images_dir = "email_images"
    os.makedirs(images_dir, exist_ok=True)
    
    # Parse the email body
    soup = BeautifulSoup(body, "html.parser")
    
    # Get attachments
    attachments = get_attachment(email['id'], token)
    
    # Download and replace image URLs with local paths
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            parsed_url = urllib.parse.urlparse(img_url)
            if not parsed_url.scheme:
                img_url = urllib.parse.urljoin("https://base.url.of.your.email.server", img_url)
            img_filename = os.path.join(images_dir, os.path.basename(parsed_url.path))
            if download_image(img_url, img_filename):
                img['src'] = img_filename
            else:
                # Handle embedded images (cid:ii_m47gc3l70)
                if img_url.startswith('cid:'):
                    cid = img_url.split(':')[1]
                    for attachment in attachments:
                        if attachment.get('contentId') == cid:
                            img_content = attachment.get('contentBytes')
                            if img_content:
                                with open(img_filename, 'wb') as f:
                                    f.write(base64.b64decode(img_content))
                                img['src'] = img_filename

    # Create HTML content with email metadata
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p><strong>From:</strong> {from_email}</p>
        <p><strong>To:</strong> {to_emails}</p>
        <p><strong>Subject:</strong> {subject}</p>
        <p><strong>Date:</strong> {received_time}</p>
        <hr>
        {str(soup)}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    options = {
        'enable-local-file-access': None
    }
    try:
        pdfkit.from_string(html_content, pdf_filename, options=options)
        print(f'PDF saved as {pdf_filename}')
    except IOError as e:
        print(f"Error saving email as PDF: {e}")

# # Example usage
# PO_KEY_WORDS = [' PO ', ' PURCHASE ORDER', ' PURCHASE_ORDER']
# extract_emails_to_pdf(PO_KEY_WORDS)
