#!/usr/bin/env python

from dashboard.fetch.daily import index_daily_data
import datetime
import logging
import sys


logging.basicConfig(level=logging.INFO)

def main(max_days_ago):
    for days_ago in range(1, max_days_ago + 1):
        date = datetime.date.today() - datetime.timedelta(days=days_ago)
        index_daily_data(date)

if __name__ == '__main__':
    # Yesterday's data is usually sampled; the day before is usually now
    # available unsampled.  Fetch the previous day's data.
    max_days_ago = 2
    if len(sys.argv) > 1:
        max_days_ago = int(sys.argv[1])
    main(max_days_ago)
