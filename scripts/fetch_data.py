#!/usr/bin/env python

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
    traffic_info = ga.fetch_traffic_info(date)
    result_clicks = ga.fetch_search_result_clicks(date)
    es.add(result_clicks, "result_clicks")
    es.add(ga.fetch_search_traffic_by_start(date, traffic_info), "search_start")

    #es.add(ga.fetch_overview_data(date))
#    es.add(ga.fetch_search_traffic_by_destination_orgs(date), "sdest_org")
#    es.add(ga.fetch_search_traffic_destination_formats(date), "sdest_org")
#    es.add(ga.fetch_page_traffic(date), "page_traffic")


def main(argv):
    try:
        import datetime
        date = datetime.date.today() - datetime.timedelta(days=2)
        index_daily_data(date)

        #pprint.pprint(ga.visits())
        #pprint.pprint(ga.fetch_overview_data(yesterday))
        #pprint.pprint(ga.fetch_search_traffic_by_start(yesterday))
        #pprint.pprint(ga.fetch_search_traffic_destination_orgs(yesterday))
        #pprint.pprint(ga.fetch_search_traffic_destination_formats(yesterday))
        #pprint.pprint(ga.fetch_per_org_overview_data(yesterday))
        #pprint.pprint(ga.fetch_search_refinements())
    except GAError:
        print "Exiting on error"


if __name__ == '__main__':
  main(sys.argv)
