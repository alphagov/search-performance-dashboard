

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
                        'query': { 'match_all': {} },
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
                'size': 1000,
            }
        )
        stats = [
            doc.get('_source', {})
            for doc in docs.get('hits', {}).get('hits', [])
        ]
        return stats

    def click_positions(self, startdate, enddate, query=None):
        filters = [
            {'type': { 'value': 'search_result_click' }},
            {
                'range': {
                    'date': {
                        'gte': startdate,
                        'lte': enddate,
                    }
                },
            }
        ]
        if query is not None:
            filters.append({
                'term': {
                    'norm_search': query
                },
            })
        body = {
            'query': {
                'filtered': {
                    'query': { 'match_all': {} },
                    'filter': {
                        'and': filters
                    },
                }
            },
            'size': 0,
            'facets': {
                'positions': {
                    'terms_stats': {
                        'key_field': 'position',
                        'value_field': 'clicks',
                        'order': 'term',
                        'size': 0,
                    }
                }
            }
        }
        result = self.es.search(
            index=self.index,
            body=body
        )
        return [
            (item['term'], item['total'])
            for item in result['facets']['positions']['terms']
        ]
