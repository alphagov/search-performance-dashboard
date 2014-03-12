#!/usr/bin/env python

import datetime
import logging
import sys

from dashboard.ga import GAData, GAError
from dashboard.esindex import ESIndex

logging.basicConfig(level=logging.INFO)


def index_daily_data(date):
    ga = GAData()
    es = ESIndex(date)
    es.clear()
    es.create_index()
    es.add(ga.fetch_search_result_clicks(date))
#    traffic_info = ga.fetch_traffic_info(date)
#    es.add(ga.fetch_search_traffic_by_start(date, traffic_info), "search_start")

#    es.add(ga.fetch_overview_data(date))
#    es.add(ga.fetch_search_traffic_by_destination_orgs(date), "sdest_org")
#    es.add(ga.fetch_search_traffic_destination_formats(date), "sdest_org")
#    es.add(ga.fetch_page_traffic(date), "page_traffic")


def main(argv):
    # Index yesterdays data; this is usually sampled.
    date = datetime.date.today() - datetime.timedelta(days=1)
    index_daily_data(date)

    # Reindex the day before; this is usually now available in unsampled form.
    date = datetime.date.today() - datetime.timedelta(days=2)
    index_daily_data(date)

if __name__ == '__main__':
  main(sys.argv)
