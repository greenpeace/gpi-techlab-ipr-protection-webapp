import datetime
import random

import pytest
from google.cloud.firestore_v1 import DocumentSnapshot

import modules.dashboard.helpers
from modules.dashboard import dashboard


class MockQueryStreamObject(DocumentSnapshot):
    def __init__(
        self,
        create_time,
        reference=None,
        data=None,
        exists=None,
        read_time=None,
        update_time=None,
    ):
        super().__init__(reference, data, exists, read_time, create_time, update_time)


random.seed(50)
list_of_dates = [
    datetime.date(2022, month, day)
    for (month, day) in zip(
        random.choices(list(range(0, 13)), k=50),
        random.choices(list(range(1, 28)), k=50),
    )
] + [datetime.date(2023, 1, 20), datetime.date(2023, 1, 5)]


@pytest.mark.parametrize(
    "current_month, current_year, expected",
    [(10, 2023, "2023_9"), (1, 2023, "2022_12"), (12, 2022, "2022_11")],
)
def test_create_previous_month(current_month, current_year, expected):
    assert expected == modules.dashboard.helpers.create_previous_month(
        current_month, current_year
    )


def test_date_count_changes():
    mock_doc_stream = [
        MockQueryStreamObject(create_time=date) for date in list_of_dates
    ]
    out = modules.dashboard.helpers.calculate_count_diff_vs_x_period_ago(
        mock_doc_stream
    )
    assert out == "-66.7%"
