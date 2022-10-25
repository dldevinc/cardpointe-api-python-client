from collections import namedtuple
from typing import Dict, TypeVar

T = TypeVar("T")


def constants(cls: T) -> T:
    """
    Decorator that converts the class to a namedtuple.
    """
    members = tuple(
        (name, value)
        for name, value in cls.__dict__.items()
        if not name.startswith("_")
    )
    klass = namedtuple("{}Type".format(cls.__name__), [record[0] for record in members])
    return klass(*[record[1] for record in members])


def clean_data(value: Dict) -> Dict:
    """
    Remove keys from dictionary with None values.
    """
    return {
        key: value
        for key, value in value.items()
        if value is not None
    }
