#!/usr/bin/env python

from dashboard.fetch.daily import index_daily_data
import datetime
import logging
import sys


logging.basicConfig(level=logging.INFO)


def main(min_days_ago, max_days_ago):
    for days_ago in range(min_days_ago, max_days_ago + 1):
        print "Fetching data for %d days ago" % (days_ago, )
        date = datetime.date.today() - datetime.timedelta(days=days_ago)
        index_daily_data(date)


if __name__ == '__main__':
    # Yesterday's data is usually sampled; the day before is usually now
    # available unsampled.  Fetch the previous day's data.
    min_days_ago = 1
    max_days_ago = 2
    if len(sys.argv) == 2:
        max_days_ago = int(sys.argv[1])
    elif len(sys.argv) == 3:
        min_days_ago = int(sys.argv[1])
        max_days_ago = int(sys.argv[2])
    elif len(sys.argv) != 1:
        print "Usage: %s [[min_days_ago] max_days_ago]" % (sys.argv[0],)
        sys.exit(1)
    main(min_days_ago, max_days_ago)
