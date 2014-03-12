import dashboard.essearch
import datetime


def get_stats():
    es = dashboard.essearch.ESSearch();
    stats = es.fetch_stats(
        datetime.date.today() - datetime.timedelta(days=7),
        datetime.date.today() - datetime.timedelta(days=1),
    )
    return stats


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_stats())
