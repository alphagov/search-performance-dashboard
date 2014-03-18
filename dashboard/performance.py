"""Methods of calculating the performance of a query.

"""

from dashboard.essearch import ESSearch
from datetime import date, timedelta
import math


# This variable holds the output of running:
# python -c '
# from dashboard import performance;
# print performance.fetch_overall_drop_rate()
# '
expected_drop_rate = [
    0.4292279309410415, 0.5765581894128737, 0.625382492350153,
    0.6013479480968028, 0.7436183790682833, 0.7488736322677537,
    0.6670964045265722, 0.8798582778612841, 0.7627821842586944,
    0.7889937609982403, 0.8623276561232766, 0.9496825770044675,
    0.7771725674671949, 0.812360624402676, 0.9576470588235294,
    0.852989352989353, 0.9735957753240518, 0.7988165680473372,
    0.8351851851851851, 0.9682187730968219, 0.8709923664122138,
    0.9351579970395594,
]


def fetch_overall_drop_rate(max_days_ago=14):
    """Calculate the current overall drop rate.

    This is the rate at which frequency of clicks decreases as we move from
    position N to N + 1, across all clicks on search results since
    `max_days_ago`.

    This can be used to update expected_drop_rate.

    """
    es = ESSearch()
    today = date.today()
    positions = es.click_positions(today - timedelta(days=max_days_ago), today)
    return calc_drop_rate(positions)


def calc_drop_rate(positions, result_len=None, min_count=1000):
    """Calculate the drop-off rate of clicks on positions.

    Returns an array of rate of clicks compared to the previous position.

    The result array is of length result_len, and the final entry represents
    the geometric mean of the drop off rates for all subsequent positions
    supplied.  The logic behind this is that the rate becomes fairly constant
    after a given point, so for the purposes of comparing to an expected drop
    its better to use a constant rate, rather than allow the variation we see
    due to the low sample size for later click posisions.

    If result_len is None, the min_count value is used to cut off the list once
    there are fewer than min_count clicks at the current position.

    """
    prev_count = positions[0][1]
    drop = []
    for pos in range(1, len(positions)):
        count = positions[pos][1]
        if prev_count == 0:
            this_drop = 1.0
        else:
            this_drop = float(count) / prev_count
        drop.append(this_drop)
        prev_count = count
        if result_len is None and min_count is not None and count < min_count:
            result_len = pos
    # Compute geometric mean of drop after result_len, since there tends not to
    # be enough data after that point to calculate individual results
    # accurately.
    drop[result_len - 1:] = [math.pow(reduce(
        lambda a, x: a * x,
        drop[result_len - 1:],
        1.0
    ), 1.0 / len(drop[result_len - 1:]))]
    return drop


def estimate_missed_clicks(counts):
    """Estimate how many more clicks we could get by reordering results.

    Returns a score that indicates roughly how many searches would be improved
    if the ordering of the results was changed such that the results were in
    sorted order by click rate.  A low score is therefore better.

    The method used is based on the assumption that the overall click position
    distribution is independent of the query results.  This is obviously a
    shaky assumption, but inaccuracy here will lead to overestimating the
    possibilities for improvement, and won't bias against particular searches
    more than others.

    Method:

     - use the expected_drop_rate to estimate how many clicks each result would
       have got were it in first place.
     - sort the resulting estimates into descending order.
     - use the expected_drop_rate to estimate how many clicks each result would
       have got were it in the resulting position.
     - compute the sum of the number of clicks in the new positions.
     - score is the difference between the sum of the number of clicks in the
       new positions, and the sum of the number of clicks actually received.

    :param counts: a list of click counts for a query, in order of ranking.

    """
    counts = [
        count if count >= 5 else 0
        for count in counts
    ]
    actual_clicks = sum(counts)

    # A measure of how good we actually think our ranking is.  This indicates
    # the ratio of how good the ranking is.
    ranking_goodness = 0.9

    compensation = []
    total_drop = 1.0
    for pos in range(len(counts)):
        compensation.append(total_drop)
        try:
            drop = expected_drop_rate[pos]
        except IndexError:
            drop = expected_drop_rate[-1]
        total_drop *= drop / ranking_goodness

    compensated = map(lambda (x, y): x / y, zip(counts, compensation))
    compensated.sort(reverse=True)
    compensated = map(lambda (x, y): x * y, zip(compensated, compensation))
    return sum(compensated) - actual_clicks
