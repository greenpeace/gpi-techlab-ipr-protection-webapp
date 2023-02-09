# Get the Flask Files Required
from functools import partial
from typing import Dict, Callable, Any, List, Tuple, Union
from modules.auth.auth import login_is_required
import json

from flask import Blueprint, render_template, request

# Set Blueprint’s name https://realpython.com/flask-blueprint/
from modules.dashboard.config import CollectionStreams, SEARCHLINK_KEYS

from modules.dashboard.helpers import (
    return_total_number_in_query_stream,
    calculate_count_diff_vs_x_period_ago,
    calculate_most_frequent_field_in_collection,
    format_data_for_flot_graph,
    construct_news_feed,
    create_country_location_counts,
)


dashboardblue = Blueprint("dashboardblue", __name__)


format_data_flot_partial = partial(
    format_data_for_flot_graph,
    query_stream=CollectionStreams.brandlinks_ref_stream.value,
)

KEY_COUNT_DICT = {
    f"searchlink_{key}_count": partial(
        calculate_most_frequent_field_in_collection,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
        key=key,
        counter_fn=value[0],
        fn_args=value[1],
    )
    for key, value in SEARCHLINK_KEYS.items()
}


@dashboardblue.route("/getdatecounts", methods=["GET"], endpoint="/getdatecounts")
def format_data_for_flot_graph() -> Dict[str, int]:
    return format_data_flot_partial()


@dashboardblue.route("/setdaterange", methods=["POST"], endpoint="setdaterange")
def format_data_for_flot_graph() -> Dict[str, int]:
    request_dict = json.loads(request.data.decode("utf-8"))
    request_dict = {
        date_range: date_str.split("T")[0]
        for date_range, date_str in request_dict.items()
    }
    min_date = request_dict.get("min_date")
    max_date = request_dict.get("max_date")
    return format_data_flot_partial(min_date=min_date, max_date=max_date)


@dashboardblue.route("/getmapdata", methods=["GET"], endpoint="/getmapdata")
def get_map_data_counts() -> Dict[str, float]:
    country_counts: List[
        Tuple[str, Union[float, int, str], float]
    ] = KEY_COUNT_DICT.get("searchlink_country_count")()
    return {
        country_name.lower(): float(count)
        for (country_name, _, count) in country_counts
        if country_name not in [None, "Not found"]
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
