# Get the Flask Files Required
import collections
from functools import partial
from typing import Dict, Callable, Any, Union, List, Tuple, Optional

from flask import Blueprint, render_template
import datetime

# Set Blueprint’s name https://realpython.com/flask-blueprint/
from modules.dashboard.config import Collections, CollectionStreams, SEARCHLINK_KEYS
import numpy as np

dashboardblue = Blueprint("dashboardblue", __name__)

from modules.auth.auth import login_is_required
from google.cloud.firestore_v1 import Query, DocumentSnapshot


def return_total_number_in_query_stream(
    query_stream: List[DocumentSnapshot],
) -> int:
    return len(query_stream) if query_stream is not None else None


def calculate_count_diff_vs_x_period_ago(
    query_stream: List[DocumentSnapshot],
) -> Union[str, None]:
    if query_stream is None:
        return None
    create_time_month = [doc.create_time.month for doc in query_stream]
    current_month = datetime.date.today().month
    if current_month == 1:
        previous_month = 12
    else:
        previous_month = current_month - 1
    previous_month_count = create_time_month.count(previous_month)
    if previous_month_count == 0:
        previous_month_count = 1.0
    return f"{np.round(100 * (create_time_month.count(current_month) - previous_month_count) / previous_month_count, 1)}%"


def calculate_most_frequent_field_in_collection(
    query_stream: List[DocumentSnapshot], key: str
) -> List[Tuple[str, int]]:
    list_of_selected_keys = [doc._data.get(key) for doc in query_stream]
    top_key_count = collections.Counter(list_of_selected_keys).most_common(5)
    return top_key_count


def create_date_array(query_stream: List[DocumentSnapshot]) -> List[datetime.date]:
    return [datetime.datetime.date(_date.create_time) for _date in query_stream]


def find_date_range(query_stream: List[DocumentSnapshot]) -> List[str]:
    datelist = create_date_array(query_stream)
    return [str(min(datelist)), str(max(datelist))]


def format_date_key_for_js_rendering(date_key: datetime.date) -> Tuple[int, int, int]:
    return date_key.year, date_key.month, date_key.day


def format_data_for_flot_graph(
    query_stream: List[DocumentSnapshot],
) -> List[Tuple[str, Tuple[int, int, int], int]]:
    datelist = create_date_array(query_stream)
    return [
        (str(key), format_date_key_for_js_rendering(key), value)
        for key, value in sorted(collections.Counter(datelist).items())
    ]


def get_latest_n_entries(
    query_stream: List[DocumentSnapshot],
    n: int = 5,
) -> List[DocumentSnapshot]:
    return sorted(query_stream, key=lambda x: x.create_time, reverse=True)[:n]


def get_info_for_news_feed(
    document_snapshot: DocumentSnapshot, news_feed_fields: Optional[List[str]] = None
):
    if news_feed_fields is None:
        news_feed_fields: List[str] = ["shop", "search", "url", "country", "category"]
    nf_dict = {}
    nf_dict["time_diff"] = (
        datetime.datetime.now(datetime.timezone.utc) - document_snapshot.create_time
    )
    return {
        **nf_dict,
        **{field: document_snapshot for field in news_feed_fields},
    }


def construct_news_feed(
    query_stream: List[DocumentSnapshot],
    n: int = 5,
):
    latest_n_entries = get_latest_n_entries(query_stream, n)
    return [get_info_for_news_feed(entry) for entry in latest_n_entries]


format_data_flot_partial = partial(
    format_data_for_flot_graph,
    query_stream=CollectionStreams.brandlinks_ref_stream.value,
)


@dashboardblue.route("/getdatecounts", methods=["GET"], endpoint="/getdatecounts")
@login_is_required
def format_data_for_flot_graph() -> Dict[str, int]:
    return format_data_flot_partial()


KEY_COUNT_DICT = {
    f"searchlink_{key}_count": partial(
        calculate_most_frequent_field_in_collection,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
        key=key,
    )
    for key in SEARCHLINK_KEYS
}

CONFIG_DICT = {
    "count_illegal_items": partial(
        return_total_number_in_query_stream,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
    ),
    "change_vs_previous_month_count_illegal_items": partial(
        calculate_count_diff_vs_x_period_ago,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
    ),
    "count_total_merch": partial(
        return_total_number_in_query_stream,
        query_stream=CollectionStreams.brandlinkdetails_ref_stream.value,
    ),
    "change_vs_previous_month_count_total_merch": partial(
        calculate_count_diff_vs_x_period_ago,
        query_stream=CollectionStreams.brandlinkdetails_ref_stream.value,
    ),
    "count_total_stopwords": partial(
        return_total_number_in_query_stream,
        query_stream=CollectionStreams.brandstopwords_ref_stream.value,
    ),
    "change_vs_previous_month_count_total_stopwords": partial(
        calculate_count_diff_vs_x_period_ago,
        query_stream=CollectionStreams.brandstopwords_ref_stream.value,
    ),
    "news_feed": partial(
        construct_news_feed, query_stream=CollectionStreams.brandlinks_ref_stream.value
    ),
    **KEY_COUNT_DICT,
}


def create_document_count_dict(
    config: Dict[str, Callable],
) -> Dict[str, Any]:
    output_dict = dict()
    for name, rendering_function in config.items():
        output_dict[name] = rendering_function()
    return output_dict


# Main page dashboard
@dashboardblue.route("/main", endpoint="main")
@login_is_required
# @track_emissions
def main():
    documents_to_render = create_document_count_dict(config=CONFIG_DICT)
    return render_template("dashboard.html", **locals(), output=documents_to_render)
