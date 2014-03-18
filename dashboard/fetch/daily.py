from dashboard.fetch.ga import GAData, GAError
from dashboard.fetch.esindex import ESIndex


def index_daily_data(date):
    """Fetch and index all the data for the given date.

    """
    ga = GAData(date)
    es = ESIndex(date)
    es.clear()
    es.create_index()
    es.add(ga.fetch_search_result_clicks())
    traffic_info = ga.fetch_traffic_info()
#    es.add(ga.fetch_search_traffic_by_start(traffic_info))

    es.add(ga.fetch_search_traffic_destination_orgs())
    es.add(ga.fetch_search_traffic_destination_formats())
