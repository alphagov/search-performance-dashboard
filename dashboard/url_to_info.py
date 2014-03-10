"""Look up information for a path on gov.uk

Fetches organisations (by analytics id) and format, and stores them in a cache.

"""

from dashboard.dirs import CACHE_DIR
import json
import logging
import os
import requests
import re
import time


logger = logging.getLogger(__name__)
org_re = re.compile('"_setCustomVar",9,"Organisations","([^"]+)",3')
format_re = re.compile('"_setCustomVar",2,"Format","([^"]+)",3')


class UrlToInfo(object):
    def __init__(self):
        self.cache_path = os.path.join(CACHE_DIR, 'urlinfo.json')
        self.cache_expiry_seconds = 3600 * 24 * 7
        self.url_info_cache = self.load()

    def load(self):
        if not os.path.exists(self.cache_path):
            return {}
        if os.path.getsize(self.cache_path) == 0:
            # Happens if an error occurred after opening for write but before
            # writing (eg, json encoding fail)
            return {}
        with open(self.cache_path) as fobj:
            return json.load(fobj)

    def save(self):
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        with open(self.cache_path + '.tmp', 'wb') as fobj:
            json.dump(self.url_info_cache, fobj)
        os.rename(self.cache_path + '.tmp', self.cache_path)

    def lookup(self, path):
        path = self.normalise_path(path)
        if path is None:
            return {}

        now = time.time()

        entry = self.url_info_cache.get(path)
        if entry is not None:
            info, created = entry
            if now - created < self.cache_expiry_seconds:
                return dict(info)
        info = self.lookup_info_by_path(path)
        self.url_info_cache[path] = info, now
        logger.info('Info for %s is %s', path, info)
        self.save()
        return dict(info)

    @staticmethod
    def normalise_path(path):
        if not path.startswith('/'):
            return None
        # Smart-answer "internal" pages have a component of "y" as the top
        # component.
        if path.endswith('/y'):
            path = path[:-2]
        else:
            path = path.split('/y/', 1)[0]
        # Ignore query parameters
        return path.split('?', 1)[0]

    def fetch_content(self, path):
        logger.info('Fetching %s', path)
        return requests.get('https://www.gov.uk%s' % path)

    def lookup_info_by_path(self, path):
        page = self.fetch_content(path)
        content = page.content
        info = {}
        mo = org_re.search(content)
        if mo:
            info['orgs'] = filter(
                None, mo.groups(1)[0].lstrip('<').rstrip('>').split('><'))

        mo = format_re.search(content)
        if mo:
            info['format'] = mo.groups(1)[0]

        return info
