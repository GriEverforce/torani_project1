# Constants

CFD_CONFIG_FILE_NAME =  'config/config.ini' 
AZURE_AD = 'azure_ad'
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
TENANT_ID = 'tenant_id'
SCOPES = 'scopes'
#
HOME_DIR = "./"
LOGGER_PATH = 'logs/'
LOGGER_FILE = f"{HOME_DIR}/{LOGGER_PATH}/logger_output.log"
REPOSITORY_FOLDER = "./repository_cfd"
ENV_FILE = 'config/cfd_env_file'
SPLIT_BOL_FOLDER = 'split_bols/'
SPLIT_INVOICE_FOLDER = 'split_invoices/'
EMAIL_BODY_PO_PDF_FILE = 'email_body_po.pdf'


# DB related
ORDER_SEQ = 'CFD_RTC_ORDER_DOC_PO_SEQ'
PO_TABLE = 'CFD_RTC_ORDER_PO_DOC'
ORDER_TABLE = 'CFD_RTC_ORDER_DOC'
PICKSLIP_TABLE = 'CFD_RTC_ORDER_PICKSLIP_DOC'
ORDER_ACK_TABLE = ORDER_TABLE
BOL_TABLE = 'CFD_RTC_ORDER_BOL_DOC'
INVOICE_TABLE = 'CFD_RTC_ORDER_INVOICE_DOC'
DEFAULT_ORDER_NUMBER = -99999
BLOB_FILES_PROCESSED = 'BLOB_FILES_PROCESSED'


# App related
BOL_STRING = "BOL"
INVOICE_STRING = "INVOICE"


# 
PO_KEY_WOPDS = ['PO ', 'PURCHASE ORDER', 'PURCHASE_ORDER', 'NEW ORDER']

MAIL_SEARCH_KEYWORDS = ["PO ", "PURCHASE_ORDER", "PURCHASE ORDER", 'NEW ORDER', # PO
                        'ORDER', 'ORDER_ACKOWLEDEGMENT', 'ORDER_CONFIRMATION',  # ORDER
                        'PICKSLIP','PICK-SLIP', 'PICK_SLIP', # PICKSLIP
                        'BOL', 'BILL OF LADING', 'BILL-OF-LADING',# BOL
                        'INVOICE' # INVOICE
                        ]

# Define the mapping of key-strings in the mail subject to table names
key_string_to_table = {

        MAIL_SEARCH_KEYWORDS[0]: 'CFD_RTC_ORDER_PO_DOC',
        MAIL_SEARCH_KEYWORDS[1]: 'CFD_RTC_ORDER_PO_DOC',
        MAIL_SEARCH_KEYWORDS[2]: 'CFD_RTC_ORDER_PO_DOC',
        MAIL_SEARCH_KEYWORDS[3]: 'CFD_RTC_ORDER_PO_DOC',
        MAIL_SEARCH_KEYWORDS[4]: 'CFD_RTC_ORDER_DOC',
        MAIL_SEARCH_KEYWORDS[5]: 'CFD_RTC_ORDER_DOC',
        MAIL_SEARCH_KEYWORDS[6]: 'CFD_RTC_ORDER_DOC',
        MAIL_SEARCH_KEYWORDS[7]: 'CFD_RTC_ORDER_PICKSLIP_DOC',
        MAIL_SEARCH_KEYWORDS[8]: 'CFD_RTC_ORDER_PICKSLIP_DOC',
        MAIL_SEARCH_KEYWORDS[9]: 'CFD_RTC_ORDER_PICKSLIP_DOC',
        MAIL_SEARCH_KEYWORDS[10]: 'CFD_RTC_ORDER_BOL_DOC',
        MAIL_SEARCH_KEYWORDS[11]: 'CFD_RTC_ORDER_BOL_DOC',
        MAIL_SEARCH_KEYWORDS[12]: 'CFD_RTC_ORDER_BOL_DOC',
        MAIL_SEARCH_KEYWORDS[13]: 'CFD_RTC_ORDER_INVOICE_DOC',
    }

# Define the blob column names
blob_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_FILE_CONTENT',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_FILE_CONTENT',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_FILE_CONTENT',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_FILE_CONTENT',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_FILE_CONTENT',
}

# Define the filename column names
filename_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_FILE_NAME',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_FILE_NAME',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_FILE_NAME',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_FILE_NAME',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_FILE_NAME',
}

# Define the date column names
date_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_DATE',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_DATE',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_DATE',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_DATE',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_DATE',
}

# Define the order num column names
doc_num_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_NUMBER',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_NUMBER',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_NUMBER',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_NUMBER',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_NUMBER',
}

# Define the FILE MIME TYPE num column names
mimetype_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_FILE_MIMETYPE',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_FILE_MIMETYPE',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_FILE_MIMETYPE',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_FILE_MIMETYPE',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_FILE_MIMETYPE',
}

# Define the FILE CHARSET num column names
charset_column_names = {
        'CFD_RTC_ORDER_PO_DOC'          : 'PO_FILE_CHARSET',
        'CFD_RTC_ORDER_DOC'             : 'ORDER_FILE_CHARSET',
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP_FILE_CHARSET',
        'CFD_RTC_ORDER_BOL_DOC'         : 'BOL_FILE_CHARSET',
        'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE_FILE_CHARSET',
}

# # Define the order num column names
# doc_num_str_name = {
#         'CFD_RTC_ORDER_PO_DOC'          : 'PO NUMBER',
#         'CFD_RTC_ORDER_DOC'             : 'ORDER NUMBER',
#         'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'PICKSLIP NUMBER',
#         'CFD_RTC_ORDER_BOL_DOC'         : 'BOL#',
#         'CFD_RTC_ORDER_INVOICE_DOC'     : 'INVOICE#',
# }

# # Define the order num column names
# order_number_strings = {
#         'CFD_RTC_ORDER_PO_DOC'          : 'DEFAULT_VALUE',
#         'CFD_RTC_ORDER_DOC'             : 'ORDER NUMBER:',
#         'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'ORDER NUMBER:',
#         'CFD_RTC_ORDER_BOL_DOC'         : 'ORDER NUMBER:',
#         'CFD_RTC_ORDER_INVOICE_DOC'     : 'ORDER NUMBER:',
# }

# # Define the doc date column names
# doc_date_strings = {
#         'CFD_RTC_ORDER_PO_DOC'          : 'PO DATE',
#         'CFD_RTC_ORDER_DOC'             : 'DATE',
#         'CFD_RTC_ORDER_PICKSLIP_DOC'    : 'DATE:',
#         'CFD_RTC_ORDER_BOL_DOC'         : 'SHIP DATE:',
#         'CFD_RTC_ORDER_INVOICE_DOC'     : 'DATE:',
# }

# We will define all the possible key strings.
# Before checking if the key sting is present, we will remove the following expected symobls after that.
# Expected symbols: '-', ':', '#'.
# Example:  It could be 'PO Number' or 'PO Number:'

symbols_to_remove = ['-', ':', '#']


# List of key strings to search for
po_number_key_strings = [
    'PO#', 'PO Number', 'Purchase Order'
]
order_number_key_strings = [
    'Order', 'Order #', 'Order Number', 'Order Confirmation Number', 'Order Acknowldgement Number'
]
pickslip_number_key_strings = [
    'PickSlip#', 'PICKSLIP#', 'Pick-slip Number', 'Pick_slip Number'
]
bol_number_key_strings = [
    'BOL#', 'BOL Number'
]
invoice_number_key_strings = [
    'Invoice Number', 'Invoice #', 'Invoice:', 'Inv. No.'
]
po_date_key_strings = [
    'PO Date', 'Purchase Order Date', 'PO Dt.'
]
po_date_key_strings = [
    'PO Date', 'Purchase Order Date', 'PO Dt.'
]
order_date_key_strings = [
    'Order Date', 'Order Confirmation', 'Order Dt.'
]
pickslip_date_key_strings = [
    'Pickslip Date', 'Pick-Slip Date', 'Pick_slip Date', 'ship date'
]
bol_date_key_strings = [
    'Date', 'BOL Date', 'bol Dt.'
]
invoice_date_key_strings = [
    'DATE', 'Invoice Date', 'Invoice Dt.'
]

# Another option for key_strings. This is not used for now.
# key_string_dict = {
#         ('PO#', 'PO Number', 'Purchase Order'): r'\d+',
#         ('Invoice Number', 'Invoice #', 'Invoice:', 'Inv. No.'): r'\d+',
#         ('PO Date', 'Purchase Order Date', 'PO Dt.'): r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{1,2}-\d{1,2}',
#         ('Invoice Date', 'Invoice Dt.'): r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{1,2}-\d{1,2}'
#     }

# Define the order num column names
doc_num_str_name = {
        'CFD_RTC_ORDER_PO_DOC'          : po_number_key_strings,
        'CFD_RTC_ORDER_DOC'             : order_number_key_strings,
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : pickslip_number_key_strings,
        'CFD_RTC_ORDER_BOL_DOC'         : bol_number_key_strings,
        'CFD_RTC_ORDER_INVOICE_DOC'     : invoice_number_key_strings,
}


# Define the order num column names
order_number_strings = {
        'CFD_RTC_ORDER_PO_DOC'          : order_number_key_strings,
        'CFD_RTC_ORDER_DOC'             : order_number_key_strings,
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : order_number_key_strings,
        'CFD_RTC_ORDER_BOL_DOC'         : order_number_key_strings,
        'CFD_RTC_ORDER_INVOICE_DOC'     : order_number_key_strings,
}


# Define the doc date column names
doc_date_strings = {
        'CFD_RTC_ORDER_PO_DOC'          : po_date_key_strings,
        'CFD_RTC_ORDER_DOC'             : order_date_key_strings,
        'CFD_RTC_ORDER_PICKSLIP_DOC'    : pickslip_date_key_strings,
        'CFD_RTC_ORDER_BOL_DOC'         : bol_date_key_strings,
        'CFD_RTC_ORDER_INVOICE_DOC'     : invoice_date_key_strings,
}

# Define patterns for numbers and dates
number_pattern = r'\d+'
# date_pattern = r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{1,2}-\d{1,2}'
date_pattern = r'\d{1,2}-[a-zA-Z]{3}-\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{4}-\d{1,2}-\d{1,2}'
