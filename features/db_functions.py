import os
import sys
import cx_Oracle
from datetime import datetime
import platform
import json
from pathlib import Path



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

# Our libraries
from env_utils import read_environment_variable
import constants
from app_logger import logger
from file_parser import extract_value_from_pdf


def exe_sql_query(db_curr, sql_qury):

    qry_response = "--did not get any response--"
    logger.info(f'sql_query : {sql_qury}')
    try:
        db_curr.execute(sql_qury)
        qry_response = db_curr.fetchall()
        # logger.info(f'sql response: {qry_response}')
        success = True
    except Exception as sql_error:
        logger.error(f"SQL Exception: {sql_error}")
        success = False
    # finally:
    #     db_curr.close()

    return(success, qry_response)


def connect_to_oracle():

    # ora_serv = read_environment_variable("EF_ORA_SERVICE_NAME", "")
    # ora_user = read_environment_variable('EF_ORA_USER', "")
    # ora_pwd = read_environment_variable('EF_ORA_PWD', "")
    # ora_port = read_environment_variable('EF_ORA_PORT', "")
    # ora_ip = '204.236.229.116' # ef_oralce on AWS

    ora_serv = read_environment_variable("CFD_ORA_SERVICE_NAME", "")
    ora_user = read_environment_variable('CFD_ORA_USER', "")
    ora_pwd  = read_environment_variable('CFD_ORA_PWD', "")
    ora_port = read_environment_variable('CFD_ORA_PORT', "")
    # ora_ip = 'paypal.cryz7xpjhcqw.us-east-2.rds.amazonaws.com'
    ora_ip = "trniusuxt053.torani.com" # Test Torani TTorani

    logger.info(f"Database URL: {ora_ip} user: {ora_user}")

    ret_result = ""

    # Oracle  connection details
    # dsn = cx_Oracle.makedsn('192.168.18.208', '1521', service_name='AEXT.dbtoolsprdphxae.dbtoolsprodprod.oraclevcn.com')  # Connection string
    dsn = cx_Oracle.makedsn(ora_ip, ora_port, service_name=ora_serv)  # Connection string
    # dsn = cx_Oracle.makedsn('dbtoolsprod-phx-apex-ext-mt-02', '1521', service_name='orclpdb')  # Connection string
    # Example DSN: cx_Oracle.makedsn('mydb.example.com', '1521', service_name='orclpdb')

    # Establishing the connection
    try:
        
        if platform.system() == "Darwin":
            # cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/Downloads/instaclient-basic-macos-arm64-23.3")
            cx_Oracle.init_oracle_client(lib_dir="/Users/gridharanvidi/oracle_client/instaclient-basic-macos-arm64-23.3")
        else:
            logger.info("platform.system() is not Darwin. May get error in accessing Orcale client library")
        # cx_Oracle.clientversion()  
        logger.info("Connecting to database...")
        connection = cx_Oracle.connect(user=ora_user, password=ora_pwd, dsn=dsn)
        logger.info("Successfully connected to database")
        logger.info(f"Database version: {connection.version}")
        
        # Create a cursor
        cursor = connection.cursor()
        
        # # Check the existing of table in Oracle 
        # sql_query = f"SELECT count(*) FROM {REPOSITORY_TABLE}"
        # sucess_yes, respones = exe_sql_query(cursor, sql_query)
        # if sucess_yes:
        #     logger.info(f"Database connection verified and table {REPOSITORY_TABLE} found ")
        
            # # Fetching and logger.infoing the results
            # for row in respones:
            #     logger.info(row)
    

    except cx_Oracle.DatabaseError as ora_err:
        logger.error(f" *** Databaes connection - Exception: {ora_err}")
        logger.error("Exiting...")
        cursor = "CONNECTION_FAILED"
        exit(1)
        # raise # Log error as appropriate
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if connection:
    #         connection.close()
    #         logger.info("Connection closed.")

    return connection



def get_column_name(column_names, doc_type):
    """
    This function returns the corresponding doc_type based on the provided document key.
    
    :param doc_key: The key for the document type (string).
    :return: Corresponding doc_type (string), or None if the key is not found.
    """
    # Check if the provided doc_key exists in the struct_doc_type dictionary
    return column_names.get(doc_type, None)  # Return None if the key is not found

# # Example usage
# doc_key = 'CFD_RTC_ORDER_BOL_DOC'  # Input key
# doc_type = get_doc_type(doc_key)

# if doc_type:
#     print(f"The document type for {doc_key} is: {doc_type}")
# else:
#     print(f"No document type found for the key: {doc_key}")




def check_and_convert_date(date_str):
    # Define possible input formats
    input_formats = [
        "%d-%b-%y",  # '29-AUG-24'
        "%d-%m-%y",  # '29-08-24'
        "%m-%d-%y",  # '08-29-24'
        "%Y-%m-%d",  # '2024-08-29'
        "%m-%d-%Y",  # '10-12-2024'
        # Add more formats as needed
    ]
    
    output_format = "%m-%d-%y"  # Desired output format ('MM-DD-YY')
    
    for fmt in input_formats:
        try:
            # Try to parse the input date string
            date_obj = datetime.strptime(date_str, fmt)
            # Convert and return the date in the desired format
            return date_obj.strftime(output_format)
        except ValueError:
            # If the format doesn't match, continue with the next format
            continue
    
    # If none of the formats match, raise an error
    # raise ValueError("Invalid date format provided.")


# # Example usage:
# input_date = "29-AUG-24"
# try:
#     formatted_date = check_and_convert_date(input_date)
#     logger.info(f"Input date: {date_str} Formatted Date: {formatted_date}")
# except ValueError as e:
#     logger.error(e)



def insert_into_cfd_repository(cursor, file_path, file_name, upload_repository_table):

    """
    Insert a PDF file into the CFD_REPOSITORY_TABLE.
    """
    with open(file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    # Extract metadata (example: mimetype and charset are placeholders)
    mime_type = "application/pdf"
    charset = "UTF-8"

    # import random
    # po_number = random.randint(100, 2000)
    # logger.info(f"po_number: {po_number}")


    blob_column = get_column_name(constants.blob_column_names, upload_repository_table)
    filename_column = get_column_name(constants.filename_column_names, upload_repository_table)
    date_column = get_column_name(constants.date_column_names, upload_repository_table)
    doc_num_column_name = get_column_name(constants.doc_num_column_names, upload_repository_table)
    doc_number_str = get_column_name(constants.doc_num_str_name, upload_repository_table)
    file_mime_type = get_column_name(constants.mimetype_column_names, upload_repository_table)
    file_charset = get_column_name(constants.charset_column_names, upload_repository_table)
    order_number_str = get_column_name(constants.order_number_strings, upload_repository_table)
    doc_date_str = get_column_name(constants.doc_date_strings, upload_repository_table)

    
    logger.info(f"{blob_column} | {filename_column} | {date_column} | {doc_number_str} | {doc_date_str}")

    doc_num_value = extract_value_from_pdf(file_path, doc_number_str, constants.number_pattern)
    if doc_num_value is None: # None not allowed
        doc_num_value = 0
    # po_date = extract_value_from_pdf(file_path, 'PO DATE')
    logger.info(f"doc_number_str: {doc_number_str} doc_num_value: {doc_num_value}")

    order_num_value = extract_value_from_pdf(file_path, order_number_str, constants.number_pattern)
    if order_num_value is None: # None not allowed
        order_num_value = 0

    doc_date_raw_value = extract_value_from_pdf(file_path, doc_date_str, constants.date_pattern)
    if doc_date_raw_value is None: # None not allowed
        doc_date_value = '01-01-1999' # TODO - Not getting the date. Needs to entered manually
    logger.info(f"doc_date_str: {doc_date_str} doc_date_raw_value: '{doc_date_raw_value}'")
    doc_date_value = check_and_convert_date(doc_date_raw_value)
    logger.info(f"doc_date_str: {doc_date_str} doc_date_value: '{doc_date_value}'")


    # For PO alone, the default order number os -99999
    if 'PO' in upload_repository_table:
        order_num_value = constants.DEFAULT_ORDER_NUMBER

    logger.info(f"order_number_str: {order_number_str} order_num_value: {order_num_value}") 


    # logger.info(f"-------< {constants.ORDER_TABLE} / {upload_repository_table}")
    # if it an order table, there is no additional ORDER_NUMBER column.
    if upload_repository_table == constants.ORDER_TABLE:

        # Define the SQL insert statement for ORDER_TABLE
        sql_q = f"""
        INSERT INTO {upload_repository_table} (
            REQ_ID, {doc_num_column_name},
            {blob_column}, {filename_column}, {date_column}, ACTIVE_FLAG,
            {file_mime_type}, {file_charset}, CREATED_BY, CREATION_DATE,
            UPDATED_BY, UPDATE_DATE
        ) VALUES (
            :REQ_ID, :{doc_num_column_name},
            :{blob_column}, :{filename_column}, to_Date(:{date_column}, 'MM-DD-YYYY'), :ACTIVE_FLAG,
            :{file_mime_type}, :{file_charset}, :CREATED_BY, SYSTIMESTAMP,
            :UPDATED_BY, SYSTIMESTAMP
        )
        """
    else:

        # Define the SQL insert statement
        sql_q = f"""
        INSERT INTO {upload_repository_table} (
            REQ_ID, {doc_num_column_name}, ORDER_NUMBER,
            {blob_column}, {filename_column}, {date_column}, ACTIVE_FLAG,
            {file_mime_type}, {file_charset}, CREATED_BY, CREATION_DATE,
            UPDATED_BY, UPDATE_DATE
        ) VALUES (
            :REQ_ID, :{doc_num_column_name}, :ORDER_NUMBER,
            :{blob_column}, :{filename_column}, to_Date(:{date_column}, 'MM-DD-YYYY'), :ACTIVE_FLAG,
            :{file_mime_type}, :{file_charset}, :CREATED_BY, SYSTIMESTAMP,
            :UPDATED_BY, SYSTIMESTAMP
        )
        """

    # Bind variables
    bind_vars = {
        'REQ_ID': 1,
        doc_num_column_name: doc_num_value,
        'ORDER_NUMBER': order_num_value,
        blob_column: pdf_data,  
        filename_column: file_name,       
        date_column: doc_date_value,
        'ACTIVE_FLAG': 'Y',
        file_mime_type: mime_type,
        file_charset: charset,
        'CREATED_BY': 'SYSTEM',
        'UPDATED_BY': 'SYSTEM'
    }

    # logger.info(f"INSERT Q: {sql_q}")
    # logger.info(f"bind_vars: {bind_vars}")

    try:
        cursor.execute(sql_q, bind_vars)
        logger.info(f"Inserted {file_name} Doc# {doc_num_value} Date: {doc_date_value} Order: {order_num_value}.")
        upload_success = True
    except cx_Oracle.DatabaseError as e:
        logger.error(f"Error inserting {file_name}: {e}")
        upload_success = False

    return upload_success

