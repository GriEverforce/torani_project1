import requests
from msal import PublicClientApplication, ConfidentialClientApplication
import msal
import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

# Our libraries
from env_utils import read_config_section
from constants import *
from app_logger import logger  # Adjust path based on the module location


# Token for Application permissions (rather than as delegated permissions)
def get_app_token():

    azure_config = read_config_section(None, AZURE_AD)
    authority = f"https://login.microsoftonline.com/{azure_config[TENANT_ID]}"

    # logger.info(f"authority: {authority}")
    app = ConfidentialClientApplication(
        azure_config[CLIENT_ID],
        authority=authority,
        client_credential=azure_config[CLIENT_SECRET],
    )

    # scope_in_config = [azure_config[SCOPES]] if isinstance(azure_config[SCOPES], str) else azure_config[SCOPES]
    # logger.info(f"azure_config[SCOPES]: {azure_config[SCOPES]}")
    scope_in_config = azure_config[SCOPES]
    logger.info(f"scope_in_config: {scope_in_config}")
    result = app.acquire_token_for_client(scopes=[scope_in_config])
    if 'access_token' in result:
        logger.info("Got token")
        return result['access_token']
    else:
        raise ValueError('Could not acquire token. Err: %s' % json.dumps(result, indent=4))


# Function to get access token using MSAL
def get_access_token():

    azure_config = read_config_section(None, AZURE_AD)
    authority = f"https://login.microsoftonline.com/{azure_config[TENANT_ID]}"

    # Initialize the MSAL app
    app = msal.ConfidentialClientApplication(
        azure_config[CLIENT_ID],
        authority=authority, 
        client_credential=azure_config[CLIENT_SECRET]
    )

    # Get token
    # result = app.acquire_token_for_client(scopes=SCOPES)
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        # logger.info(f"access_token: {result["access_token"]}")
        logger.info("Successfully received 'access token'")
        return result["access_token"]
    else:
        logger.error(f"Error obtaining access token: {result.get('error_description')}")
        return None
    

def get_access_token_using_refresh_token():
    
    # URL for token exchange
    token_url = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/token'

    # Set the data to be sent in the POST request to refresh the token
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }

    # Send the POST request to refresh the token
    result = requests.post(token_url, data=data)

    # Check the response
    if result.status_code == 200:
        # Successful token refresh
        token_data = result.json()
        access_token = token_data['access_token']
        # logger.info(f"Refreshed access token: {access_token}")
        logger.info(f"Refreshed access token: Got it")
    else:
        # Handle error cases
        logger.error(f" ********* Error: {result.status_code}, {result.text} ***")
        access_token = None

    return access_token

def get_token():

    azure_config = read_config_section(None, AZURE_AD)
    AUTHORITY = f"https://login.microsoftonline.com/{azure_config[TENANT_ID]}"

    # AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
    app = PublicClientApplication(
        azure_config[CLIENT_ID],
        authority=AUTHORITY,
    )
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise ValueError('Fail to create device flow. Err: %s' % json.dumps(flow, indent=4))
    logger.info(flow['message'])

    result = app.acquire_token_by_device_flow(flow)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise ValueError('Could not acquire token. Err: %s' % json.dumps(result, indent=4))