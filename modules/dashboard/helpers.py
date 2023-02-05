import collections
import datetime
from functools import partial
from typing import List, Union, Tuple, Callable, Optional

import numpy as np
from google.cloud.firestore_v1 import DocumentSnapshot


def return_total_number_in_query_stream(
    query_stream: List[DocumentSnapshot],
) -> int:
    return len(query_stream) if query_stream is not None else None


def create_previous_month(current_month: int, current_year: int) -> str:
    if current_month == 1:
        previous_year_month = f"{current_year - 1}_{12}"
    else:
        previous_year_month = f"{current_year}_{current_month - 1}"
    return previous_year_month


def calculate_count_diff_vs_x_period_ago(
    query_stream: List[DocumentSnapshot],
) -> Union[str, None]:
    if query_stream is None:
        return None
    create_year_month = [
        f"{doc.create_time.year}_{doc.create_time.month}" for doc in query_stream
    ]
    current_year_month, current_month, current_year = (
        f"{datetime.date.today().year}_{datetime.date.today().month}",
        datetime.date.today().month,
        datetime.date.today().year,
    )
    previous_year_month = create_previous_month(current_month, current_year)
    previous_month_count = create_year_month.count(previous_year_month)
    if previous_month_count == 0:
        previous_month_count = 1.0
    return f"{np.round(100 * (create_year_month.count(current_year_month) - previous_month_count) / previous_month_count, 1)}%"


def calculate_most_frequent_field_in_collection(
    query_stream: List[DocumentSnapshot], key: str
) -> List[Tuple[str, int]]:
    list_of_selected_keys = [doc._data.get(key) for doc in query_stream]
    return collections.Counter(list_of_selected_keys).most_common(5)


def create_item_array(
    query_stream: List[DocumentSnapshot], fn: Callable, attr: str
) -> List[datetime.date]:
    return [fn(getattr(_date, attr)) for _date in query_stream]


def find_date_range(query_stream: List[DocumentSnapshot]) -> List[str]:
    datelist = create_item_array(
        query_stream, fn=datetime.datetime.date, attr="create_time"
    )
    return [str(min(datelist)), str(max(datelist))]


def format_date_key_for_js_rendering(date_key: datetime.date) -> Tuple[int, int, int]:
    return date_key.year, date_key.month, date_key.day


def format_data_for_flot_graph(
    query_stream: List[DocumentSnapshot],
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
) -> List[Tuple[str, Tuple[int, int, int], int]]:
    datelist = create_item_array(
        query_stream, fn=datetime.datetime.date, attr="create_time"
    )
    if min_date is None:
        min_date = min(datelist)
    else:
        min_date = datetime.datetime.strptime(min_date, "%Y-%m-%d").date()
    if max_date is None:
        max_date = max(datelist)
    else:
        max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d").date()
    datelist = [date for date in datelist if max_date >= date >= min_date]
    return [
        (str(key), format_date_key_for_js_rendering(key), value)
        for key, value in sorted(collections.Counter(datelist).items())
    ]


def get_top_n_entries(
    query_stream: List[DocumentSnapshot],
    key_sort_fn: Callable,
    n: int = 5,
) -> List[DocumentSnapshot]:
    return sorted(query_stream, key=key_sort_fn, reverse=True)[:n]


def get_info_for_news_feed(
    document_snapshot: DocumentSnapshot, news_feed_fields: Optional[List[str]] = None
):
    if news_feed_fields is None:
        news_feed_fields: List[str] = ["shop", "search", "url", "country", "category"]
    nf_dict = {}
    time_diff_raw = (
        datetime.datetime.now(datetime.timezone.utc) - document_snapshot.create_time
    )
    nf_dict["time_diff"] = (
        f"{time_diff_raw.total_seconds()//3600 - 24.0} hours ago"
        if time_diff_raw.days < 1
        else f"{time_diff_raw.days} day(s) ago"
    )
    return {
        **nf_dict,
        **{field: document_snapshot._data.get(field) for field in news_feed_fields},
    }


def construct_news_feed(
    query_stream: List[DocumentSnapshot],
    n: int = 5,
):
    latest_n_entries = get_top_n_entries(
        query_stream, key_sort_fn=lambda x: x.create_time, n=n
    )
    return [get_info_for_news_feed(entry) for entry in latest_n_entries]


def gettr(x, key):
    return x.get(key)


partialed_gettr_country = partial(gettr, key="country")


def create_country_location_counts(
    query_stream: List[DocumentSnapshot],
):
    country_item_list = create_item_array(
        query_stream, fn=partialed_gettr_country, attr="country"
    )
    return {
        key: value
        for key, value in sorted(collections.Counter(country_item_list).items())
    }
