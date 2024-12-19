import logging
import os
import sys

# Add the path to the 'features' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import constants

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)



def check_log_folder():
    # Ensure the directory exists before creating the file
    log_directory = os.path.dirname(constants.LOGGER_PATH)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        logger.info(f"Created directory: {log_directory}")


def check_create_logfile():

    # Assuming constants.LOGGER_FILE holds the path to the log file
    logger_file_path = constants.LOGGER_FILE

    # Check if the log file exists
    if not os.path.exists(logger_file_path):
        # If the file doesn't exist, create it
        try:
            with open(logger_file_path, 'w') as f:
                # Optionally, write some initial content (e.g., headers, default settings, etc.)
                f.write("Log file created.\n")
            print(f"Log file created: {logger_file_path}")
        except Exception as e:
            print(f"Error creating log file: {e}")
    else:
        print(f"Log file already exists: {logger_file_path}")


# Create file handler
file_handler = logging.FileHandler(constants.LOGGER_FILE)
file_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)


# Log Rotation (Optional):
# To prevent the logger_output.log file from growing too large, you can use Python's logging.handlers.RotatingFileHandler.
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler("logs/logger_output.log", maxBytes=5*1024*1024, backupCount=3)

# Configure logging 
logging.basicConfig( 
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    # format='%(asctime)s - %(levelname)s - %(message)s',
    # format='%(levelname)s | %(name)s - %(process)d | %(message)s',
    format='%(levelname)s-%(filename)s-%(funcName)s:%(lineno)d - %(message)s',  # Custom format
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[ logging.FileHandler('logger_output.log'), logging.StreamHandler() ] )

# logging.basicConfig(
#     level=logging.DEBUG,  # Set the logging level
#     format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - Line: %(lineno)d - %(message)s',  # Custom format
#     handlers=[
#         logging.FileHandler("logs/logger_output.log"),  # Log to a file
#         logging.StreamHandler()  # Log to console
#     ]
# )