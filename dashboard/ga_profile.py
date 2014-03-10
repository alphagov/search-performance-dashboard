"""Look up a profile id.

"""

import hashlib
import json
import os
from dashboard.dirs import SECRETS_DIR


def get_account_id(service, account_name):
    """Get a Google Analytics account for a user by name.

    :param service: A service object; get from
    dashboard.ga_auth.initialise_service.

    :param account_name: The account name to lookup.

    """

    # Note; if a user has very many accounts, it may be necessary to page
    # through the results.  I don't have very many accounts, so am not
    # implementing that for now.  See
    # https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accounts/list
    # for details.
    accounts = service.management().accounts().list().execute()
    for account in accounts.get('items', ()):
        if account.get('name') == account_name:
            return account.get('id')
    raise KeyError("No analytics account found of name %r" % (account_name,))


def get_profile(service, account_name, property_id, profile_name):
    """Get a Google Analytics account for a user by name.

    :param service: A service object; get from
    dashboard.ga_auth.initialise_service.

    :param account_name: The account name to lookup.

    :param property_id: The property ID containing the profile.

    :param profile_name: The name of the profile to use.

    """
    profile_hash = hashlib.sha1("%s:%s:%s" % (
        account_name, property_id, profile_name)).hexdigest()
    profile_file = os.path.join(SECRETS_DIR, "profile_%s.json" % profile_hash)
    if os.path.exists(profile_file):
        with open(profile_file) as fobj:
            return json.load(fobj)
    
    account_id = get_account_id(service, account_name)

    profiles = service.management().profiles().list(
        accountId=account_id,
        webPropertyId=property_id,
    ).execute()

    for profile in profiles.get('items'):
        if profile.get('name') == profile_name:
            result = {
                'account_name': account_name,
                'account_id': account_id,
                'property_id': property_id,
                'profile_name': profile_name,
                'profile_id': profile.get('id'),
            }
            with open(profile_file, "wb") as fobj:
                json.dump(result, fobj)
            return result

    raise KeyError("No profile found of name %r" % profile_name)
