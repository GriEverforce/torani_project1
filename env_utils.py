from dotenv import load_dotenv
import os
import sys
import configparser


# Add the path to the 'features' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import constants
from app_logger import logger

# Access the constant defined in constants.py
# logger.info(constants.CFD_CONFIG_FILE_NAME)

# Load environment variables from a .env file
load_dotenv()  # It will automatically look for a .env file in the current directory

def read_environment_variable(variable_name, default_value=None):
    """
    Reads an environment variable by its name, with an optional default value.
    """
    value = os.getenv(variable_name, default_value)
    if value is None:
        logger.info(f"Warning: Environment variable '{variable_name}' is not set.")
    # logger.info(f"Environment variable '{variable_name}' is '{value}")
    return value

# Usage example
# client_id = read_environment_variable('CLIENT_ID')
# client_secret = read_environment_variable('CLIENT_SECRET')
# tenant_id = read_environment_variable('TENANT_ID')
# redirect_uri = read_environment_variable('REDIRECT_URI', 'http://localhost:55874')  # Default redirect_uri

# Output the values (or None if not found)
# logger.info(f"Client ID: {client_id}")
# logger.info(f"Client Secret: {client_secret}")
# logger.info(f"Tenant ID: {tenant_id}")
# logger.info(f"Redirect URI: {redirect_uri}")




# Flag to check if .env has already been loaded
# Efficiency: This approach ensures that the .env file is loaded only once, improving performance, especially for larger .env files or when calling the function multiple times.
# Cleaner Code: It avoids redundant operations and keeps your code efficient and clean.
_env_loaded = False

def old_read_environment_variable(env_file, variable_name, default_value=None):
    """
    Reads an environment variable from a .env file (loaded only once).

    :param env_file: The path to the .env file.
    :param variable_name: The name of the environment variable to read.
    :param default_value: The default value to return if the environment variable is not found. Default is None.
    :return: The value of the environment variable or the default value if not found.
    """
    global _env_loaded

    # Load environment variables only once
    if not _env_loaded:
        load_dotenv(dotenv_path=env_file)  # Load from the specified .env file
        _env_loaded = True  # Set the flag to indicate that the .env has been loaded
    
    # Get the value of the environment variable
    value = os.getenv(variable_name, default_value)
    
    if value is None:
        logger.info(f"Warning: Environment variable '{variable_name}' is not set.")
    
    return value


# # Usage Example:
# env_file = '.env'  # Path to your .env file
# variable_name = 'CLIENT_ID'  # Example environment variable name

# # Read the variable from the .env file
# client_id = read_environment_variable(env_file, variable_name)

# logger.info(f"Client ID: {client_id}")




def read_azure_config(config_file='config.ini'):
    """
    Reads the Azure AD configuration from a .ini file and returns the settings as a dictionary.
    
    :param config_file: The path to the .ini file. Default is 'config.ini'.
    :return: A dictionary containing the Azure AD configuration values.
    """
    config = configparser.ConfigParser()
    
    # Read the configuration file
    config.read(config_file)
    
    # Ensure that the [azure_ad] section exists
    if 'azure_ad' not in config.sections():
        raise ValueError(f"The section 'azure_ad' is missing in the config file {config_file}.")
    
    # Get the Azure AD values from the file
    azure_config = {
        'client_id': config.get('azure_ad', 'client_id'),
        'client_secret': config.get('azure_ad', 'client_secret'),
        'tenant_id': config.get('azure_ad', 'tenant_id'),
        'redirect_uri': config.get('azure_ad', 'redirect_uri'),
        'scopes': config.get('azure_ad', 'scopes')
    }

    logger.info(f"azure_config: {azure_config}")
    return azure_config


def read_config_section(given_config_file, section):
    """
    Reads the specified section from the given .ini configuration file.

    :param config_file: Path to the .ini configuration file.
    :param section: The section name to read from the configuration file.
    :return: A dictionary containing the key-value pairs from the specified section.
    """
    section_data = {}

    if not given_config_file:
        config_file = read_environment_variable(constants.ENV_FILE, constants.CFD_CONFIG_FILE_NAME)
        if not config_file: # CFD_CONFIG_FILE_NAME is not defined in env. Consider the default
            logger.info(f"Not defined env varialbe 'CFD_CONFIG_FILE_NAME'. Considering the default({constants.CFD_CONFIG_FILE_NAME})")
            config_file = constants.CFD_CONFIG_FILE_NAME
    # logger.info(f"Reading Section '{section}' in the config file '{config_file}'.")
    # Check if the file exists
    if not os.path.isfile(config_file):
        logger.info(f"*** ERROR config file '{config_file}' not found")
    else:
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read(config_file)

        # Check if the section exists
        if section not in config.sections():
            raise ValueError(f"The section '{section}' is not found in the config file '{config_file}'.")

        # Get the section data as a dictionary
        section_data = {key: config.get(section, key) for key in config.options(section)}

        # for key, value in section_data.items():
        #     logger.info(f"{key} = {value}")

    return section_data

# # Usage Example:
# config_file = '../config/config.ini'  # Path to your .ini file
# section_name = 'azure_adZZZ'  # Specify the section you want to read

# config_file = read_environment_variable('config/cfd_env', 'CFD_CONFIG_FILE_NAME')
# if not config_file: # CFD_CONFIG_FILE_NAME is not defined in env. Consider the default
#     logger.info(f"Not defined env varialbe 'CFD_CONFIG_FILE_NAME'. Considering the default({constants.CFD_CONFIG_FILE_NAME})")
#     config_file = constants.CFD_CONFIG_FILE_NAME

# Get the data from the section
# try:
#     section_data = read_config_section(config_file, section_name)
#     if not section_data:  # Evaluates True if the list is empty
#         logger.info(f"No data found - section: '{section_name}' config_file:'{config_file}'")
#     else:
#         logger.info(f"Data from section '{section_name}':")
#         for key, value in section_data.items():
#             logger.info(f"{key} = {value}")
# except ValueError as e:
#     logger.info(e)
