from dashboard.dirs import LOOKUPS_DIR
import os
import csv

ORG_FILE_NAME = 'govuk-organisation-analytics-identifiers.csv'


def read_orgs():
    orgs = {}
    with open(os.path.join(LOOKUPS_DIR, ORG_FILE_NAME)) as fobj:
        reader = csv.reader(fobj)
        reader.next()
        for analytics_id, org_id, short_name, name in reader:
            assert analytics_id not in orgs
            orgs[analytics_id] = {
                'id': org_id,
                'short_name': short_name,
                'name': name,
            }
    return orgs

ORGS = read_orgs()
