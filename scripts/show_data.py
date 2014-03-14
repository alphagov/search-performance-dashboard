import dashboard.essearch
import datetime


def get_stats():
    es = dashboard.essearch.ESSearch()
    stats = es.fetch_stats(
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=1),
    )
    return stats


def click_positions(query=None):
    es = dashboard.essearch.ESSearch()
    return es.click_positions(query)


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_stats())
    pprint.pprint(click_positions())
    pprint.pprint(click_positions('jobs'))
    pprint.pprint(click_positions('visa'))
