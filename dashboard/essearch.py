

from elasticsearch import Elasticsearch
import logging


logger = logging.getLogger(__name__)


class ESSearch(object):
    def __init__(self):
        self.es = Elasticsearch()

    def search_start_by_org(self):
        index = 'search_dashboard'
        return self.es.search(index=index, body={
            'query': {
                'match_all': {}
            },
            'sort': [
                {
                    'views': { 'order': 'desc' },
                }
            ],
        })

    def search_at_least_one_click_rate(self, startdate, enddate):
        """Return an hourly timeseries of rate at which queries get >=1 click.

        Precisely, this is sum(sessions in which the search was performed) /
        sum(sessions in which a page is viewed by clicking on a result)

        """

    def hourly_stats(self, startdate, enddate, organisations=(), formats=(),
            path_prefix=None)
