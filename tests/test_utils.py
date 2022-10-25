from cardpointe.utils import clean_data


def test_clean_data():
    assert clean_data({
        "name": "Jon",
        "empty_str": "",
        "zero": 0,
        "none": None
    }) == {
        "name": "Jon",
        "empty_str": "",
        "zero": 0,
    }
