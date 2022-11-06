from enum import Enum

from system.firstoredb import brandlinks_ref, brandlinkdetails_ref


class Collections(Enum):
    brandlinks_ref = brandlinks_ref
    brandlinkdetails_ref = brandlinkdetails_ref


class CollectionStreams(Enum):
    brandlinks_ref_stream = brandlinks_ref.stream()
    brandlinkdetails_ref_stream = brandlinkdetails_ref.stream()
