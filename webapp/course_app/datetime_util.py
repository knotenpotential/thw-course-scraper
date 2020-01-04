import arrow


def iso_ts_to_naive_utc(iso_ts):
    return arrow.get(iso_ts).naive
