#!/usr/bin/python
"""Handle authentication with google.

"""

import gapy.client
import oauth2client.tools
import os
from dashboard.dirs import SECRETS_DIR

# The file with the OAuth 2.0 Client details.  This should be a "Client ID for
# native application", which can be created and downloaded at the google
# developers console (https://console.developers.google.com).
CLIENT_SECRETS = os.path.join(SECRETS_DIR, 'client_secrets.json')

# A file which will be used to store the generated tokens produced after the
# oauth flow succeeds.  This should be kept secret, and includes a refresh
# token to refresh the oauth authorisation when required.
CLIENT_STORAGE = os.path.join(SECRETS_DIR, 'storage.json')


def perform_auth():
    """Authenticate with the GA API.

    Returns a gapy.Client object.

    """
    # Prevent oauth2client from trying to open a browser
    # This is run from inside the VM so there is no browser
    oauth2client.tools.FLAGS.auth_local_webserver = False

    # We only want to request readonly access to analytics.  gapy doesn't have
    # any way to request this other than by monkeypatching it, sadly.
    gapy.client.GOOGLE_API_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"

    return gapy.client.from_secrets_file(
        CLIENT_SECRETS,
        storage_path=CLIENT_STORAGE,
    )
