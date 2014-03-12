
from dashboard.dirs import CONFIG_DIR
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import elasticsearch.exceptions
import json
import logging
import os


logger = logging.getLogger(__name__)


class ESIndex(object):
    def __init__(self, date):
        self.date = date
        self.index_name = 'search_dashboard_%04d%02d%02d' % (
            date.year, date.month, date.day,
        )
        self.es = Elasticsearch()

        mappings_path = os.path.join(CONFIG_DIR, "mappings.json")
        self.mappings = json.load(open(mappings_path))
        settings_path = os.path.join(CONFIG_DIR, "settings.json")
        self.settings = json.load(open(settings_path))

    def clear(self):
        try:
            self.es.indices.delete(self.index_name)
        except elasticsearch.exceptions.NotFoundError:
            pass

    def create_index(self):
        self.es.indices.create(self.index_name, {
            'settings': self.settings,
        })
        for type, mapping in self.mappings.items():
            self.es.indices.put_mapping(
                index=self.index_name,
                doc_type=type,
                body={type: mapping})
        self.es.indices.put_alias(self.index_name, 'search_dashboard')

    def add(self, docs, type):
        if not self.es.indices.exists(self.index_name):
            self.create_index()
        def mk_bulk(docs):
            for doc in docs:
                doc['_type'] = type
                yield doc
        count = 0
        for result in streaming_bulk(
            self.es,
            mk_bulk(docs),
            raise_on_error=True,
            index=self.index_name
        ):
            count += 1
        logger.info("Added %d docs", count)
