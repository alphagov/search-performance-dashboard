Search performance dashboard
============================

To keep track of how well site search is serving users, this dashboard
aggregates information about site search, and presents clear metrics on how
well site search works.

The dashboard gathers information from Google Analytics (and in future is
expected to gather information from other sources such as the external link
tracker), analyses it and stores it in an elasticsearch index.  It then
provides access to computed KPIs and more specific information via an HTTP
interface and API.

Installation
------------

Requires python 2.7.

    virtualenv ENV
    . ENV/bin/activate
    pip install -r requirements.txt

Run the script to download data, daily (ideally at around 8am, to give google
analytics time to process the data from the previous day).

    python scripts/fetch_data.py
