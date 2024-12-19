import logging
import os
import sys

# Add the path to the 'features' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
from constants import *

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)



def check_and_create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Folder doesn't exist, so create it
        os.makedirs(folder_path)
        logger.info(f"Folder '{folder_path}' did not exist, so it has been created.")
    else:
        # Folder exists
        logger.info(f"Folder '{folder_path}' already exists and will be used.")

# # Example usage
# folder_path = REPOSITORY_FOLDER
# check_and_create_folder(folder_path)


def setup_folders():
    check_and_create_folder(REPOSITORY_FOLDER)