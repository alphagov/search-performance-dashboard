

from elasticsearch import Elasticsearch
import logging


logger = logging.getLogger(__name__)


class ESSearch(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'search_dashboard'

    def fetch_stats(self, startdate, enddate):
        """Return an hourly timeseries of rate at which queries get >=1 click.

        Precisely, this is sum(sessions in which the search was performed) /
        sum(sessions in which a page is viewed by clicking on a result)

        """
        docs = self.es.search(
            index=self.index,
            body={
                'query': {
                    'filtered': {
                        'query': {
                            'match_all': {}
                        },
                        'filter': {
                            'and': [
                                {
                                    'type': {
                                        'value': 'result_click_stats',
                                    },
                                },
                                {
                                    'range': {
                                        'date': {
                                            'gte': startdate,
                                            'lte': enddate,
                                        }
                                    },
                                }
                            ]
                        }
                    }
                },
                'sort': [
                    {
                        'date': { 'order': 'asc' },
                    }
                ],
            }
        )
        stats = [
            doc.get('_source', {})
            for doc in docs.get('hits', {}).get('hits', [])
        ]
        return stats
