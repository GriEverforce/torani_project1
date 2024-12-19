import msal
import requests
from datetime import datetime


def save_email_body_to_pdf(email, pdf_filename):
    body = email['body']['content']
    subject = email['subject']
    from_email = email['from']['emailAddress']['address']
    to_emails = ", ".join([recipient['emailAddress']['address'] for recipient in email['toRecipients']])
    received_time = email['receivedDateTime'][:10]  # Format YYYY-MM-DD

    # # Generate PDF file name
    # pdf_filename = f'{received_time}_{subject}.pdf'
    
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
        {body}
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
