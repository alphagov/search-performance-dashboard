#!/usr/bin/python
"""Handle authentication with google.

"""

import argparse
import httplib2
import os
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser
from dashboard.dirs import SECRETS_DIR

# The file with the OAuth 2.0 Client details.
CLIENT_SECRETS = os.path.join(SECRETS_DIR, 'client_secrets.json')

# A helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message=MISSING_CLIENT_SECRETS_MESSAGE,
)

# A file to store the access token
TOKEN_FILE_NAME = os.path.join(SECRETS_DIR, 'analytics.dat')


def prepare_credentials():
    """Retrieve existing credentials, or run the auth flow to get new ones.
    
    """
    storage = Storage(TOKEN_FILE_NAME)
    credentials = storage.get()
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[argparser],
    )
    flags = parser.parse_args(sys.argv[1:])
    if credentials is None or credentials.invalid:
        credentials = run_flow(FLOW, storage, flags)
    return credentials


def initialise_service():
    http = httplib2.Http()
    credentials = prepare_credentials()
    http = credentials.authorize(http)
    return build('analytics', 'v3', http=http)
