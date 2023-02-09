from collections import Counter
from enum import Enum
from typing import List, Dict, Tuple, Any, Union
from system.firstoredb import brandlinks_ref, brandlinkdetails_ref, brandstopwords_ref

HUNDRED = 100
THOUSAND = HUNDRED * 10


class Collections(Enum):
    brandlinks_ref = brandlinks_ref
    brandlinkdetails_ref = brandlinkdetails_ref
    brandstopwords_ref = brandstopwords_ref


class CollectionStreams(Enum):
    brandlinks_ref_stream = list(brandlinks_ref.stream())
    brandlinkdetails_ref_stream = list(brandlinkdetails_ref.stream())
    brandstopwords_ref_stream = list(brandstopwords_ref.stream())


duplicate_keys: List[Tuple] = [
    ("United States", "US"),
    ("Japan", "JP"),
    ("Canada", "CA"),
    ("Not Found", "Not found"),
    ("Australia", "AU"),
    ("Austria", "AT"),
    ("Brazil", "BR"),
    ("Bulgaria", "BG"),
    ("France", "FR"),
    ("Germany", "DE"),
    ("India", "IN"),
    ("Indonesia", "ID"),
    ("Ireland", "IE"),
    ("Hong Kong", "HK"),
    ("Netherlands", "NL"),
    ("Poland", "PL"),
    ("Russia", "RU"),
    ("Switzerland", "CH"),
    ("Sweden", "SK"),
    ("Turkey", "TR"),
    ("United Kingdom", "GB"),
]


def clean_counter_of_duplicate_keys(counter: Counter) -> Counter:
    counter_copy = counter.copy()
    for key, value in duplicate_keys:
        counter_copy[value] += counter_copy[key]
        counter_copy.pop(key)
    return counter_copy


def calculate_counter_proportions(
    counter: Counter,
) -> List[Tuple[str, Union[float, int, str], float]]:
    counter_without_duplicates = clean_counter_of_duplicate_keys(counter)
    total = sum(counter_without_duplicates.values())
    return [
        (
            key,
            f"{int(value / total * HUNDRED)}%",
            float(value / total * HUNDRED) * THOUSAND,
        )
        for key, value in counter_without_duplicates.most_common(
            len(counter_without_duplicates)
        )
    ]


SEARCHLINK_KEYS: Dict[str, Tuple[str, Dict[str, Any]]] = {
    "shop": ("most_common", {"n": 5}),
    "country": (calculate_counter_proportions, {}),
}
