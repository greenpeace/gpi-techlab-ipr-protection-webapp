# Get the Flask Files Required
from functools import partial
from typing import Dict, Callable, Any, Union

from flask import Blueprint, render_template
import datetime

# Set Blueprint’s name https://realpython.com/flask-blueprint/
from modules.dashboard.config import CollectionStreams

dashboardblue = Blueprint("dashboardblue", __name__)

from modules.auth.auth import login_is_required
from google.cloud.firestore_v1 import Query


def return_total_number_in_query_stream(
    query_stream: Query.stream,
) -> int:
    return len(list(query_stream)) if query_stream is not None else None


def find_count_diff_vs_x_period_ago(query_stream: Query.stream) -> Union[str, None]:
    if query_stream is None:
        return None
    create_time_month = [doc.create_time.month for doc in list(query_stream)]
    current_month = datetime.date.today().month
    if current_month == 1:
        previous_month = 12
    else:
        previous_month = current_month - 1
    previous_month_count = create_time_month.count(previous_month)
    if previous_month_count == 0:
        previous_month_count = 1.0
    return f"{100 * (create_time_month.count(current_month) - previous_month_count) / previous_month_count}%"


CONFIG_DICT = {
    "count_illegal_items": partial(
        return_total_number_in_query_stream,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
    ),
    "change_vs_previous_month_count_illegal_items": partial(
        find_count_diff_vs_x_period_ago,
        query_stream=CollectionStreams.brandlinks_ref_stream.value,
    ),
    "count_total_merch": partial(
        return_total_number_in_query_stream,
        query_stream=CollectionStreams.brandlinkdetails_ref_stream.value,
    ),
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
