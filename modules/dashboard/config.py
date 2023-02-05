from enum import Enum
from typing import List

from system.firstoredb import brandlinks_ref, brandlinkdetails_ref, brandstopwords_ref


class Collections(Enum):
    brandlinks_ref = brandlinks_ref
    brandlinkdetails_ref = brandlinkdetails_ref
    brandstopwords_ref = brandstopwords_ref


class CollectionStreams(Enum):
    brandlinks_ref_stream = list(brandlinks_ref.stream())
    brandlinkdetails_ref_stream = list(brandlinkdetails_ref.stream())
    brandstopwords_ref_stream = list(brandstopwords_ref.stream())


SEARCHLINK_KEYS: List[str] = ["shop", "country"]
