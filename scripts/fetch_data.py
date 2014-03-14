#!/usr/bin/env python

from dashboard.fetch.daily import index_daily_data
import datetime
import logging
import sys


logging.basicConfig(level=logging.INFO)


def main(argv):
    # Index yesterdays data; this is usually sampled.
    date = datetime.date.today() - datetime.timedelta(days=1)
    index_daily_data(date)

    # Reindex the day before; this is usually now available in unsampled form.
    date = datetime.date.today() - datetime.timedelta(days=2)
    index_daily_data(date)


if __name__ == '__main__':
    main(sys.argv)
