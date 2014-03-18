

from elasticsearch import Elasticsearch
import logging


logger = logging.getLogger(__name__)


class ESSearch(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'search_dashboard'

    @staticmethod
    def _date_range_filter(startdate, enddate):
        return {
            'range': {
                'date': {
                    'gte': startdate,
                    'lte': enddate,
                }
            }
        }

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
                                {'type': { 'value': 'result_click_stats' }},
                                self._date_range_filter(startdate, enddate),
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
            self._date_range_filter(startdate, enddate),
        ]
        if query is not None:
            filters.append({
                'term': { 'norm_search': query },
            })
        body = {
            'query': {
                'filtered': {
                    'query': { 'match_all': {} },
                    'filter': { 'and': filters },
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
        positions = dict(
            (item['term'], item['total'])
            for item in result['facets']['positions']['terms']
        )
        max_position = max(positions.keys())
        return [
            (position, positions.get(position, 0))
            for position in range(1, max_position + 1)
        ]

    def poor_searches(self, startdate, enddate):
        filters = [
            {'type': { 'value': 'search_stats' }},
            self._date_range_filter(startdate, enddate),
        ]
        body = {
            'query': {
                'filtered': {
                    'query': { 'match_all': {} },
                    'filter': { 'and': filters },
                }
            },
            'size': 0,
            'facets': {
                'positions': {
                    'terms_stats': {
                        'key_field': 'norm_search',
                        'value_field': 'missed',
                        'order': 'total',
                        'size': 20,
                    }
                }
            }
        }
        result = self.es.search(
            index=self.index,
            body=body
        )
        return [
            {
                "norm_search": item['term'],
                "missed": item['total'],
            }
            for item in result['facets']['positions']['terms']
        ]
