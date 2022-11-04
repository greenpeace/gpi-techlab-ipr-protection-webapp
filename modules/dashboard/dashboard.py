# Get the Flask Files Required
from functools import partial
from typing import List, Dict, Callable, Any

from flask import Blueprint, g, request, render_template
import datetime

# Carbon tracking
# from codecarbon import track_emissions

# Set Blueprint’s name https://realpython.com/flask-blueprint/
from system.firstoredb import brandlinks_ref, brandlinkdetails_ref

dashboardblue = Blueprint("dashboardblue", __name__)

from modules.auth.auth import login_is_required
from google.cloud.firestore_v1 import CollectionReference

# unpack total number of docs
def unpack_doc_and_return_total_number(
    firestore_collection: CollectionReference,
) -> int:
    return len(list(firestore_collection.stream()))


def find_count_diff_vs_x_period_ago(firestore_collection: CollectionReference):
    create_time_month = [
        doc.create_time.month for doc in list(firestore_collection.stream())
    ]
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
        unpack_doc_and_return_total_number, firestore_collection=brandlinks_ref
    ),
    "change_vs_previous_month_count_illegal_items": partial(
        find_count_diff_vs_x_period_ago, firestore_collection=brandlinks_ref
    ),
    "count_total_merch": partial(
        unpack_doc_and_return_total_number, firestore_collection=brandlinkdetails_ref
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
