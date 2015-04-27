#!/usr/bin/env bash
#
# Runs the fetch_data.py script every morning at 8am.
#
# This is a poor-man's cron, and is just intended to be used on the local box
# in our office.  Any future deploy of this dashboard on more "production"
# hardware should do this more sensibly.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. "${DIR}/../ENV/bin/activate"

while :; do

# Fetch the last week's data (unsampled data that was previously returned will
# be retrieved from the cache.
PYTHONPATH="${DIR}/.." "${DIR}/fetch_data.py" 28

echo "Waiting until 8am for next fetch"
sleep `python -c 'import datetime;
d=datetime.date.today();
print(
    int((
        datetime.datetime(d.year, d.month, d.day, 8)
        + datetime.timedelta(days=1)
        - datetime.datetime.now()
    ).total_seconds())
)'`

done
